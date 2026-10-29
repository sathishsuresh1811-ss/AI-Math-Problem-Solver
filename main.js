/**
 * Main application JavaScript.
 * Manages modal interactions, human review overrides, toasts, and LaTeX rendering.
 */

document.addEventListener("DOMContentLoaded", function () {
  // Render math formulas if KaTeX is available
  renderMath();

  // Setup modal close listeners
  document.querySelectorAll("[data-close-modal]").forEach(btn => {
    btn.addEventListener("click", closeModal);
  });

  // Setup click outside modal dialog to close
  const modalBackdrop = document.getElementById("resultModal");
  if (modalBackdrop) {
    modalBackdrop.addEventListener("click", function (e) {
      if (e.target === modalBackdrop) {
        closeModal();
      }
    });
  }
});

function renderMath() {
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false }
      ],
      throwOnError: false
    });
  }
}

function showToast(message, type = "success") {
  const container = document.getElementById("toastContainer") || createToastContainer();
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.style.cssText = `
    background: ${type === "success" ? "#065f46" : type === "error" ? "#7f1d1d" : "#1e293b"};
    color: #fff;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
    margin-top: 10px;
    font-size: 13px;
    border: 1px solid rgba(255,255,255,0.1);
    animation: fadeIn 0.2s ease;
  `;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3500);
}

function createToastContainer() {
  const c = document.createElement("div");
  c.id = "toastContainer";
  c.style.cssText = "position: fixed; bottom: 20px; right: 20px; z-index: 9999;";
  document.body.appendChild(c);
  return c;
}

function copyToClipboard(text, alertMsg = "Copied to clipboard!") {
  navigator.clipboard.writeText(text).then(() => {
    showToast(alertMsg);
  }).catch(() => {
    showToast("Failed to copy", "error");
  });
}

function openResultModal(resultId) {
  const modal = document.getElementById("resultModal");
  if (!modal) return;

  fetch(`/api/result/${resultId}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("modalResultId").textContent = data.id;
      document.getElementById("modalProblemId").textContent = data.problem_id;
      document.getElementById("modalTopic").textContent = `${data.topic} • ${data.difficulty}`;
      document.getElementById("modalProvider").textContent = `${data.provider} (${data.model})`;
      document.getElementById("modalCondition").textContent = data.prompt_condition.replace('_', ' ').toUpperCase();
      
      const statusBadge = document.getElementById("modalStatusBadge");
      if (data.is_correct === 1) {
        statusBadge.className = "badge badge-success";
        statusBadge.textContent = "Verified Correct";
      } else if (data.is_correct === 0) {
        statusBadge.className = "badge badge-danger";
        statusBadge.textContent = "Incorrect";
      } else {
        statusBadge.className = "badge badge-warning";
        statusBadge.textContent = "Needs Review";
      }

      document.getElementById("modalStatement").textContent = data.statement;
      document.getElementById("modalRefAnswer").textContent = data.reference_answer;
      document.getElementById("modalParsedAnswer").textContent = data.parsed_answer || "(None parsed)";
      document.getElementById("modalAIResponse").textContent = data.ai_response;

      // Populate step evaluations
      const stepsContainer = document.getElementById("modalStepsContainer");
      stepsContainer.innerHTML = "";
      if (data.step_evaluations && data.step_evaluations.length > 0) {
        data.step_evaluations.forEach(s => {
          const div = document.createElement("div");
          div.className = `step-item step-${s.status}`;
          div.innerHTML = `
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
              <strong>Step ${s.step_number}: ${s.step_description}</strong>
              <span class="badge ${s.score === 1.0 ? 'badge-success' : s.score === 0.5 ? 'badge-warning' : 'badge-danger'}">
                Score: ${s.score}
              </span>
            </div>
            <div style="font-size: 12px; color: #94a3b8;">${s.feedback || ''}</div>
          `;
          stepsContainer.appendChild(div);
        });
      } else {
        stepsContainer.innerHTML = "<div style='color:#64748b;'>No granular step evaluations recorded.</div>";
      }

      // Populate error classifications
      const errorsContainer = document.getElementById("modalErrorsContainer");
      errorsContainer.innerHTML = "";
      if (data.error_classifications && data.error_classifications.length > 0) {
        data.error_classifications.forEach(e => {
          const div = document.createElement("div");
          div.style.cssText = "background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239,68,68,0.25); border-radius:6px; padding:10px; margin-bottom:8px;";
          div.innerHTML = `
            <div style="display:flex; justify-content:space-between; font-weight:600; color:#f87171; font-size:13px;">
              <span>${e.category}</span>
              <span style="text-transform:uppercase; font-size:10px;">${e.severity} severity</span>
            </div>
            <div style="font-size:12px; color:#cbd5e1; margin-top:4px;">${e.evidence}</div>
          `;
          errorsContainer.appendChild(div);
        });
      } else {
        errorsContainer.innerHTML = "<div style='color:#10b981; font-size:13px;'>No errors detected in this execution.</div>";
      }

      // Pre-fill human review form
      document.getElementById("reviewResultId").value = data.id;
      if (data.corrected_is_correct !== null && data.corrected_is_correct !== undefined) {
        document.getElementById("reviewScoreSelect").value = data.corrected_is_correct;
      } else {
        document.getElementById("reviewScoreSelect").value = data.is_correct !== null ? data.is_correct : "0";
      }
      document.getElementById("reviewNotes").value = data.review_notes || "";

      modal.classList.add("active");
      renderMath();
    })
    .catch(err => {
      showToast("Error loading result details", "error");
    });
}

function closeModal() {
  const modal = document.getElementById("resultModal");
  if (modal) {
    modal.classList.remove("active");
  }
}

function submitHumanReview(e) {
  e.preventDefault();
  const resId = document.getElementById("reviewResultId").value;
  const score = parseInt(document.getElementById("reviewScoreSelect").value, 10);
  const reviewer = document.getElementById("reviewerName").value || "Evaluator";
  const notes = document.getElementById("reviewNotes").value;

  fetch("/api/human-review", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      result_id: resId,
      corrected_is_correct: score,
      reviewer_name: reviewer,
      notes: notes
    })
  })
    .then(res => res.json())
    .then(data => {
      showToast("Human review saved successfully!");
      closeModal();
      // Reload current page if on results view to reflect changes
      if (window.location.pathname === "/results") {
        setTimeout(() => window.location.reload(), 800);
      }
    })
    .catch(() => {
      showToast("Failed to save human review", "error");
    });
}
