/**
 * Experiment Runner JavaScript.
 * Controls problem selection, provider/condition toggles, batch execution,
 * and live progress logging.
 */

document.addEventListener("DOMContentLoaded", function () {
  updateRunCounter();

  // Listen for changes on selection checkboxes
  const checkBoxes = document.querySelectorAll(".problem-checkbox, .provider-checkbox, .condition-checkbox");
  checkBoxes.forEach(cb => {
    cb.addEventListener("change", updateRunCounter);
  });

  // Filter problems in runner
  const topicFilter = document.getElementById("expTopicFilter");
  const diffFilter = document.getElementById("expDiffFilter");
  if (topicFilter) topicFilter.addEventListener("change", filterProblemList);
  if (diffFilter) diffFilter.addEventListener("change", filterProblemList);

  // Select all / deselect all
  const selectAllBtn = document.getElementById("selectAllProblems");
  const deselectAllBtn = document.getElementById("deselectAllProblems");
  if (selectAllBtn) {
    selectAllBtn.addEventListener("click", () => {
      document.querySelectorAll(".problem-row:not([style*='display: none']) .problem-checkbox").forEach(cb => cb.checked = true);
      updateRunCounter();
    });
  }
  if (deselectAllBtn) {
    deselectAllBtn.addEventListener("click", () => {
      document.querySelectorAll(".problem-checkbox").forEach(cb => cb.checked = false);
      updateRunCounter();
    });
  }

  // Run Experiment Form
  const runForm = document.getElementById("experimentRunForm");
  if (runForm) {
    runForm.addEventListener("submit", handleRunExperiment);
  }
});

function filterProblemList() {
  const topic = document.getElementById("expTopicFilter").value.toLowerCase();
  const diff = document.getElementById("expDiffFilter").value.toLowerCase();
  const rows = document.querySelectorAll(".problem-row");

  rows.forEach(r => {
    const rowTopic = r.dataset.topic.toLowerCase();
    const rowDiff = r.dataset.difficulty.toLowerCase();
    const matchTopic = !topic || rowTopic === topic;
    const matchDiff = !diff || rowDiff === diff;
    if (matchTopic && matchDiff) {
      r.style.display = "";
    } else {
      r.style.display = "none";
    }
  });
  updateRunCounter();
}

function updateRunCounter() {
  const selProblems = document.querySelectorAll(".problem-row:not([style*='display: none']) .problem-checkbox:checked").length;
  const selProviders = document.querySelectorAll(".provider-checkbox:checked").length;
  const selConditions = document.querySelectorAll(".condition-checkbox:checked").length;
  const totalRuns = selProblems * selProviders * selConditions;

  const countBadge = document.getElementById("totalRunsBadge");
  if (countBadge) {
    countBadge.textContent = `${totalRuns} Total Trials`;
  }
  const runBtn = document.getElementById("startExperimentBtn");
  if (runBtn) {
    runBtn.disabled = (totalRuns === 0);
  }
}

function handleRunExperiment(e) {
  e.preventDefault();

  const problemIds = Array.from(document.querySelectorAll(".problem-row:not([style*='display: none']) .problem-checkbox:checked")).map(cb => cb.value);
  const providerKeys = Array.from(document.querySelectorAll(".provider-checkbox:checked")).map(cb => cb.value);
  const conditions = Array.from(document.querySelectorAll(".condition-checkbox:checked")).map(cb => cb.value);

  if (problemIds.length === 0 || providerKeys.length === 0 || conditions.length === 0) {
    showToast("Please select at least 1 problem, 1 provider, and 1 condition.", "error");
    return;
  }

  const runBtn = document.getElementById("startExperimentBtn");
  const progressArea = document.getElementById("experimentProgressArea");
  const logConsole = document.getElementById("experimentLogConsole");
  const progressBar = document.getElementById("experimentProgressBar");
  const progressText = document.getElementById("experimentProgressText");

  runBtn.disabled = true;
  runBtn.textContent = "Running Trials...";
  progressArea.style.display = "block";
  logConsole.innerHTML = "";
  progressBar.style.width = "10%";
  progressText.textContent = `Initializing trial batch for ${problemIds.length} problem(s)...`;

  const log = (msg) => {
    const item = document.createElement("div");
    item.style.cssText = "padding: 3px 0; border-bottom: 1px solid rgba(255,255,255,0.03);";
    item.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
    logConsole.appendChild(item);
    logConsole.scrollTop = logConsole.scrollHeight;
  };

  log(`Dispatched run request: ${problemIds.length} problems across ${providerKeys.length} providers.`);
  progressBar.style.width = "40%";

  fetch("/api/run-experiment", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      problem_ids: problemIds,
      provider_keys: providerKeys,
      conditions: conditions,
      name: document.getElementById("experimentName").value || "Custom Experiment Trial"
    })
  })
    .then(res => res.json())
    .then(data => {
      progressBar.style.width = "100%";
      progressText.textContent = `Batch Completed: ${data.successful_runs} of ${data.total_runs} trials finished.`;
      log(`Execution complete. Saved experiment ID: ${data.experiment_id}`);
      
      data.results.forEach(r => {
        const statusText = r.is_correct === 1 ? "CORRECT" : r.is_correct === 0 ? "INCORRECT" : "UNSCORABLE";
        log(`Problem ${r.problem_id} [${r.provider} - ${r.condition}]: ${statusText} (Step Acc: ${r.step_accuracy}%)`);
      });

      showToast(`Batch completed: ${data.successful_runs} runs recorded.`);
      runBtn.textContent = "Completed!";
      
      // Add view results button
      const actionsDiv = document.getElementById("postRunActions");
      if (actionsDiv) {
        actionsDiv.style.display = "flex";
      }
    })
    .catch(err => {
      progressBar.style.backgroundColor = "#ef4444";
      progressText.textContent = "Error executing experiment batch.";
      log(`Error: ${err.message}`);
      showToast("Experiment execution failed", "error");
      runBtn.disabled = false;
      runBtn.textContent = "Retry Experiment";
    });
}
