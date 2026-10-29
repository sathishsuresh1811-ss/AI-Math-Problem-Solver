/**
 * Charts JavaScript Module using Chart.js.
 * Sets up academic data visualizations with dark-mode aesthetic styling.
 */

// Global Chart.js defaults
if (window.Chart) {
  Chart.defaults.color = "#94a3b8";
  Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
  Chart.defaults.plugins.legend.labels.usePointStyle = true;
  Chart.defaults.plugins.tooltip.backgroundColor = "rgba(15, 23, 42, 0.95)";
  Chart.defaults.plugins.tooltip.borderColor = "rgba(255, 255, 255, 0.1)";
  Chart.defaults.plugins.tooltip.borderWidth = 1;
  Chart.defaults.plugins.tooltip.padding = 10;
}

function initDashboardCharts(promptData, topicData) {
  // 1. Prompt Condition Comparison Bar Chart
  const promptCtx = document.getElementById("promptCompChart");
  if (promptCtx && promptData) {
    new Chart(promptCtx, {
      type: "bar",
      data: {
        labels: ["Plain Baseline", "Step-by-Step Reasoning", "Self-Verification"],
        datasets: [
          {
            label: "Final-Answer Accuracy (%)",
            data: [
              promptData.plain.final_accuracy,
              promptData.step_by_step.final_accuracy,
              promptData.self_verification.final_accuracy
            ],
            backgroundColor: "rgba(99, 102, 241, 0.8)",
            borderRadius: 6
          },
          {
            label: "Mean Step Accuracy (%)",
            data: [
              promptData.plain.mean_step_accuracy,
              promptData.step_by_step.mean_step_accuracy,
              promptData.self_verification.mean_step_accuracy
            ],
            backgroundColor: "rgba(6, 182, 212, 0.8)",
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            grid: { color: "rgba(255, 255, 255, 0.05)" }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }
}

function initAnalyticsCharts(data) {
  if (!data) return;

  // 1. Provider Comparison Chart
  const provCtx = document.getElementById("providerCompChart");
  if (provCtx && data.by_provider) {
    const labels = data.by_provider.map(p => p.label);
    const accData = data.by_provider.map(p => p.final_accuracy);
    const stepData = data.by_provider.map(p => p.mean_step_accuracy);

    new Chart(provCtx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Final Accuracy (%)",
            data: accData,
            backgroundColor: "rgba(99, 102, 241, 0.8)",
            borderRadius: 6
          },
          {
            label: "Mean Step Accuracy (%)",
            data: stepData,
            backgroundColor: "rgba(16, 185, 129, 0.8)",
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: "rgba(255, 255, 255, 0.05)" } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // 2. Topic Performance Chart
  const topicCtx = document.getElementById("topicPerformanceChart");
  if (topicCtx && data.by_topic) {
    new Chart(topicCtx, {
      type: "bar",
      data: {
        labels: data.by_topic.map(t => t.label),
        datasets: [
          {
            label: "Final Accuracy (%)",
            data: data.by_topic.map(t => t.final_accuracy),
            backgroundColor: "rgba(6, 182, 212, 0.8)",
            borderRadius: 6
          },
          {
            label: "Step Accuracy (%)",
            data: data.by_topic.map(t => t.mean_step_accuracy),
            backgroundColor: "rgba(245, 158, 11, 0.8)",
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: "rgba(255, 255, 255, 0.05)" } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // 3. Error Categories Doughnut Chart
  const errCtx = document.getElementById("errorCategoryChart");
  if (errCtx && data.errors && data.errors.length > 0) {
    const palette = [
      "#ef4444", "#f97316", "#f59e0b", "#eab308", "#84cc16",
      "#10b981", "#06b6d4", "#3b82f6", "#6366f1", "#8b5cf6", "#ec4899"
    ];
    new Chart(errCtx, {
      type: "doughnut",
      data: {
        labels: data.errors.map(e => e.category),
        datasets: [
          {
            data: data.errors.map(e => e.count),
            backgroundColor: palette.slice(0, data.errors.length),
            borderColor: "#111827",
            borderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "right" }
        }
      }
    });
  }

  // 4. Verification Before vs After Comparison
  const verifCtx = document.getElementById("verifBeforeAfterChart");
  if (verifCtx && data.verif) {
    new Chart(verifCtx, {
      type: "bar",
      data: {
        labels: ["Pre-Verification", "Post-Verification"],
        datasets: [
          {
            label: "Final Answer Accuracy (%)",
            data: [data.verif.pre_verification_accuracy, data.verif.post_verification_accuracy],
            backgroundColor: [
              "rgba(148, 163, 184, 0.7)",
              "rgba(99, 102, 241, 0.85)"
            ],
            borderRadius: 8
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, max: 100, grid: { color: "rgba(255, 255, 255, 0.05)" } },
          x: { grid: { display: false } }
        }
      }
    });
  }
}
