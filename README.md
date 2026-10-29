# AI Math Problem Explainer and Error Checker
**College Capstone Project — Evaluating AI Mathematical Reasoning Reliability & Self-Verification**

---

## 1. Project Overview

The **AI Math Problem Explainer and Error Checker** is an end-to-end full-stack academic research dashboard that rigorously evaluates how reliably AI systems solve and explain school and college mathematics step by step.

The system tests multiple AI providers across three prompt conditions:
1. **Plain Zero-Shot Prompt**: Direct baseline asking for the answer.
2. **Step-by-Step Chain-of-Thought Prompt**: Explicit request for formula citation and intermediate derivations.
3. **Self-Verification Prompt**: Dual-phase prompt prompting the model to derive an answer, then independently verify or critique its own result via substitution or an alternative method.

### Key Highlights
- **Curated 30-Problem Verified Benchmark**: 10 Algebra, 10 Probability & Statistics, and 10 Calculus Basics problems spanning Easy, Medium, and Hard difficulties with canonical formulas, reference steps, common misconceptions, and acceptable equivalent answer formats.
- **Dual-Metric Evaluation Engine**:
  - **Final-Answer Accuracy**: 1 (Correct), 0 (Incorrect), -1 (Unscorable / Human Review). Verified with safe symbolic and numeric equivalence matching via SymPy (strictly avoiding dangerous `eval()`).
  - **Step Accuracy**: Granular score of intermediate reasoning fidelity (0.0% to 100.0%).
- **11-Category Mathematical Error Taxonomy**: Empirical error classification with observable linguistic rubrics (e.g. *Confident but incorrect reasoning*, *Arithmetic slip*, *Probability-rule error*).
- **Self-Verification Before/After Analysis**: Measures whether self-verification fixed slips, introduced new errors, or suffered from confirmation bias.
- **Multi-Tab Spreadsheet Automation**: Exports 10-sheet Excel (`.xlsx`) workbooks formatted with formulas (`COUNTIF`, `AVERAGE`), auto-filters, frozen headers, and percentage formatting.
- **Printable 14-Section Capstone Report & 7-Slide Defense Presentation Deck**: Ready for live college evaluation and demonstration.
- **100% Functional in Demo Baseline Mode**: Starts immediately with deterministic baseline benchmark data without paid API keys.

---

## 2. Technology Stack

- **Backend**: Python 3.12, Flask 3.1
- **Database**: SQLite (ACID compliant with foreign keys and query indexes)
- **Mathematical Computation & Scoring**: SymPy (Safe AST symbolic simplification and numeric equivalence)
- **Data Processing & Analytics**: Python, pandas
- **Frontend**: Semantic HTML5, Vanilla CSS3 (Glassmorphism & High-Contrast Design System), Vanilla JavaScript (ES6+)
- **Mathematical Notation Rendering**: KaTeX (LaTeX math rendering)
- **Interactive Visualizations**: Chart.js 4.4
- **Spreadsheet Generation**: openpyxl
- **Automated Testing**: pytest

---

## 3. Project Directory Structure

```
AI-Math-Checker/
├── app.py                     # Flask web server and API endpoints
├── config.py                  # Environment configuration and provider checking
├── database.py                # SQLite schema, indexing, and baseline seeding
├── models.py                  # Structured data models
├── math_dataset.py            # Verified 30-problem benchmark dataset
├── prompt_templates.py        # Standardized prompt conditions (A, B, C)
├── ai_providers.py            # Live REST providers (ChatGPT, Gemini, Claude) & Local Demo Solver
├── answer_checker.py          # SymPy-backed equivalence checker without eval()
├── scoring.py                 # Step scoring, error taxonomy, and self-verification deltas
├── analytics.py               # Aggregations, topic breakdown, and heatmap data
├── export_service.py          # 10-sheet styled XLSX workbook & CSV generator
├── report_generator.py        # 14-section formal academic capstone report compiler
├── requirements.txt           # Python dependency requirements
├── .env.example               # Environment variables template
├── README.md                  # Comprehensive documentation
├── run.bat                    # One-click Windows startup script
├── tests/
│   ├── conftest.py            # Test suite discovery configuration
│   ├── test_dataset.py        # Dataset validation tests
│   ├── test_answer_checker.py # Numeric & symbolic equivalence tests
│   └── test_scoring.py        # Step evaluation & error classification tests
├── data/
│   ├── math_checker.db        # SQLite database file (created on launch)
│   └── README.md
├── exports/
│   └── README.md              # Exported XLSX and CSV files
├── templates/
│   ├── base.html              # Responsive layout, sidebar, KaTeX, modal review
│   ├── index.html             # Dashboard with summary stats and quick charts
│   ├── problems.html          # Problem catalog with filters
│   ├── problem_detail.html    # Problem steps, formulas, and run history
│   ├── experiment.html        # Experiment runner (single and batch)
│   ├── results.html           # Results table with human review overrides
│   ├── analytics.html         # Chart.js visualizations & problem heatmap
│   ├── error_analysis.html    # 11-category error taxonomy & evidence log
│   ├── prompt_library.html    # Prompt templates viewer and copy tools
│   ├── verification_report.html # Before/after self-verification comparison
│   ├── presentation.html      # 7-slide capstone presentation deck
│   ├── about.html             # Methodology & Responsible AI principles
│   └── report.html            # 14-section downloadable/printable report
└── static/
    ├── css/
    │   └── style.css          # Design system & print optimization
    ├── js/
    │   ├── main.js            # Modal, LaTeX, toast notifications
    │   ├── charts.js          # Chart.js charts initialization
    │   └── experiment.js      # Experiment runner controls & batch logger
    └── images/
```

---

## 4. Setup and Execution (Windows)

Follow these step-by-step instructions in Windows PowerShell or Command Prompt:

### Step 1: Open Terminal in Project Directory
```powershell
cd "c:\Users\SURESH\AI . MATH PROBLEM SOLVER"
```

### Step 2: (Optional) Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the template file to `.env`:
```powershell
Copy-Item .env.example .env
```
*(The system runs in full demo mode without API keys. To test live commercial models, add your keys to `.env`)*

### Step 5: Run Automated Tests
```powershell
python -m pytest tests/
```
All 14 tests across dataset integrity, SymPy equivalence, and error classification should pass.

### Step 6: Start the Web Application
Using the startup batch script:
```cmd
run.bat
```
Or directly via Python:
```powershell
python app.py
```

### Step 7: Access the Dashboard
Open your web browser and navigate to:
```
http://127.0.0.1:5050
```

---

## 5. Live AI Integration (Optional)

The application supports live evaluations via official REST APIs. To enable live models, edit your `.env` file:

```env
# OpenAI
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini

# Google Gemini
GEMINI_API_KEY=your-gemini-key-here
GEMINI_MODEL=gemini-1.5-flash

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
```

> **Transparency Note**: The application strictly separates live API calls from baseline demo data. The local reference solver is always clearly designated as `Local Reference Solver (Demo Baseline)`.

---

## 6. How to Export Data and Reports

1. **Excel Workbook (`.xlsx`)**:
   - Click **Export XLSX** in the top navigation header, or visit `http://127.0.0.1:5000/export/xlsx`.
   - Generates a styled 10-tab workbook with formulas, auto-filters, and frozen headers.
2. **CSV Datasets**:
   - Click **Export CSV** in the top navigation header or visit `http://127.0.0.1:5000/export/csv`.
3. **Formal Capstone PDF Report**:
   - Navigate to **Capstone Report** in the sidebar (`/report`) and click **Print / Save as PDF**.
4. **Slide Deck Presentation**:
   - Navigate to **7-Slide Deck** (`/presentation`) for fullscreen defense presentation with interactive speaker notes.

---

## 7. Responsible AI & Research Limitations

- **Arithmetic Slip Prone**: LLMs are statistical language models, not formal algebraic engines.
- **Decoupling Answers from Steps**: A correct final answer can be obtained through flawed steps, and an incorrect final answer often contains sound intermediate work.
- **Verification Bias**: Prompting an AI to self-verify does not guarantee error correction; models can exhibit circular reasoning that reinforces initial errors.
- **Human Oversight**: Results flagged as `-1` (unscorable/ambiguous) must be reviewed by human evaluators.
