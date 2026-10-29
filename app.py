"""
AI Math Problem Explainer and Error Checker.
Flask Application Server.
"""

import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for

from config import Config
from database import (
    init_db,
    get_db,
    get_all_problems_db,
    get_problem_db,
    get_all_results_db,
    get_result_detail_db
)
from ai_providers import get_provider, list_providers_status
from prompt_templates import format_prompt, get_all_templates
from answer_checker import extract_answer_candidate, evaluate_final_answer
from scoring import evaluate_steps, classify_errors, analyze_self_verification
import analytics
import export_service
import report_generator

app = Flask(__name__)
app.config.from_object(Config)

# Ensure database is initialized on startup
with app.app_context():
    init_db(seed_baseline=True)

# -----------------------------------------------------------------------------
# Web Page Routes
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    """Main Dashboard with summary cards and quick benchmarks."""
    results = get_all_results_db()
    metrics = analytics.compute_overall_metrics(results)
    prompt_comp = analytics.compute_prompt_comparison(results)
    verif = analytics.compute_self_verification_analysis(results)
    providers = list_providers_status()
    recent_results = results[:6]
    return render_template(
        "index.html",
        metrics=metrics,
        prompt_comp=prompt_comp,
        verif=verif,
        providers=providers,
        recent_results=recent_results,
        active_page="dashboard"
    )

@app.route("/problems")
def problems_view():
    """Problem Set Catalog (30 verified problems)."""
    topic_filter = request.args.get("topic")
    diff_filter = request.args.get("difficulty")
    problems = get_all_problems_db()
    
    if topic_filter:
        problems = [p for p in problems if p["topic"].lower() == topic_filter.lower()]
    if diff_filter:
        problems = [p for p in problems if p["difficulty"].lower() == diff_filter.lower()]
        
    return render_template(
        "problems.html",
        problems=problems,
        current_topic=topic_filter,
        current_difficulty=diff_filter,
        active_page="problems"
    )

@app.route("/problem/<prob_id>")
def problem_detail(prob_id):
    """Problem Details with steps, formulas, and trial history."""
    problem = get_problem_db(prob_id)
    if not problem:
        return redirect(url_for("problems_view"))
        
    # Get all runs for this problem
    conn = get_db()
    runs = conn.execute("""
    SELECT * FROM experiment_results
    WHERE problem_id = ?
    ORDER BY timestamp DESC
    """, (prob_id.upper(),)).fetchall()
    conn.close()
    
    return render_template(
        "problem_detail.html",
        problem=problem,
        runs=[dict(r) for r in runs],
        active_page="problems"
    )

@app.route("/experiment")
def experiment_view():
    """Experiment Runner (Single trial and Batch runs)."""
    problems = get_all_problems_db()
    providers = list_providers_status()
    templates = get_all_templates()
    return render_template(
        "experiment.html",
        problems=problems,
        providers=providers,
        templates=templates,
        active_page="experiment"
    )

@app.route("/results")
def results_view():
    """Results Table with filters and human review modal."""
    filters = {
        "topic": request.args.get("topic"),
        "difficulty": request.args.get("difficulty"),
        "provider": request.args.get("provider"),
        "prompt_condition": request.args.get("condition"),
        "is_correct": request.args.get("is_correct"),
        "search": request.args.get("search")
    }
    # Clean empty filters
    filters = {k: v for k, v in filters.items() if v not in [None, ""]}
    results = get_all_results_db(filters)
    return render_template(
        "results.html",
        results=results,
        filters=filters,
        active_page="results"
    )

@app.route("/analytics")
def analytics_view():
    """Analytics Dashboard with interactive Chart.js charts."""
    results = get_all_results_db()
    overall = analytics.compute_overall_metrics(results)
    by_provider = analytics.compute_by_dimension(results, "provider")
    by_topic = analytics.compute_by_dimension(results, "topic")
    by_difficulty = analytics.compute_by_dimension(results, "difficulty")
    prompt_comp = analytics.compute_prompt_comparison(results)
    verif = analytics.compute_self_verification_analysis(results)
    errors = analytics.compute_error_distribution()
    heatmap = analytics.compute_heatmap_matrix(results)
    
    return render_template(
        "analytics.html",
        overall=overall,
        by_provider=by_provider,
        by_topic=by_topic,
        by_difficulty=by_difficulty,
        prompt_comp=prompt_comp,
        verif=verif,
        errors=errors,
        heatmap=heatmap,
        active_page="analytics"
    )

@app.route("/error-analysis")
def error_analysis_view():
    """Deep-dive Error Analysis page across the 11 error categories."""
    errors = analytics.compute_error_distribution()
    conn = get_db()
    recent_errors = conn.execute("""
    SELECT ec.*, r.problem_id, r.provider, r.prompt_condition, r.parsed_answer,
           p.statement, p.final_answer as reference_answer
    FROM error_classifications ec
    JOIN experiment_results r ON ec.result_id = r.id
    JOIN problems p ON r.problem_id = p.id
    ORDER BY ec.id DESC
    LIMIT 50
    """).fetchall()
    conn.close()
    
    return render_template(
        "error_analysis.html",
        errors=errors,
        recent_errors=[dict(e) for e in recent_errors],
        active_page="error_analysis"
    )

@app.route("/prompt-library")
def prompt_library_view():
    """Prompt Library for viewing, testing, copying, and comparing templates."""
    templates = get_all_templates()
    problems = get_all_problems_db()
    return render_template(
        "prompt_library.html",
        templates=templates,
        sample_problem=problems[0] if problems else None,
        active_page="prompt_library"
    )

@app.route("/verification-report")
def verification_report_view():
    """Dedicated Self-Verification Before/After Comparison Page."""
    results = get_all_results_db()
    verif = analytics.compute_self_verification_analysis(results)
    
    # Get sample cases of fixed, introduced, and unchanged runs
    conn = get_db()
    fixed_cases = conn.execute("""
    SELECT r.*, p.statement, p.final_answer as reference_answer
    FROM experiment_results r
    JOIN problems p ON r.problem_id = p.id
    WHERE r.prompt_condition = 'self_verification' AND r.verification_fixed_error = 1
    LIMIT 5
    """).fetchall()
    
    introduced_cases = conn.execute("""
    SELECT r.*, p.statement, p.final_answer as reference_answer
    FROM experiment_results r
    JOIN problems p ON r.problem_id = p.id
    WHERE r.prompt_condition = 'self_verification' AND r.verification_fixed_error = -1
    LIMIT 5
    """).fetchall()
    conn.close()
    
    return render_template(
        "verification_report.html",
        verif=verif,
        fixed_cases=[dict(c) for c in fixed_cases],
        introduced_cases=[dict(c) for c in introduced_cases],
        active_page="verification_report"
    )

@app.route("/presentation")
def presentation_view():
    """Seven-slide Capstone Presentation Deck with live data injection."""
    results = get_all_results_db()
    metrics = analytics.compute_overall_metrics(results)
    prompt_comp = analytics.compute_prompt_comparison(results)
    verif = analytics.compute_self_verification_analysis(results)
    by_provider = analytics.compute_by_dimension(results, "provider")
    errors = analytics.compute_error_distribution()
    
    return render_template(
        "presentation.html",
        metrics=metrics,
        prompt_comp=prompt_comp,
        verif=verif,
        by_provider=by_provider,
        errors=errors,
        active_page="presentation"
    )

@app.route("/about")
def about_view():
    """About & Responsible AI Methodology Page."""
    providers = list_providers_status()
    return render_template(
        "about.html",
        providers=providers,
        active_page="about"
    )

@app.route("/report")
def report_view():
    """Downloadable / Printable 14-Section Capstone Report."""
    report_data = report_generator.compile_final_report_data()
    return render_template(
        "report.html",
        report=report_data,
        active_page="report"
    )

@app.route("/health")
def health_check():
    """Health check endpoint for liveness probes."""
    return jsonify({"status": "healthy", "service": "ai-math-checker", "timestamp": datetime.now().isoformat()}), 200

# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------

@app.route("/api/run-experiment", methods=["POST"])
def api_run_experiment():
    """Execute single trial or batch experiment."""
    data = request.get_json() or {}
    problem_ids = data.get("problem_ids", [])
    provider_keys = data.get("provider_keys", ["demo"])
    conditions = data.get("conditions", ["plain", "step_by_step", "self_verification"])
    
    if not problem_ids:
        return jsonify({"error": "No problems selected"}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    exp_id = f"exp-{uuid.uuid4().hex[:8]}"
    now_str = datetime.now().isoformat()
    total_runs = len(problem_ids) * len(provider_keys) * len(conditions)
    
    cursor.execute("""
    INSERT INTO experiments (id, name, created_at, status, total_runs, successful_runs, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        exp_id,
        data.get("name", f"Experiment Run ({len(problem_ids)} problems x {len(provider_keys)} providers)"),
        now_str,
        "running",
        total_runs,
        0,
        data.get("notes", "Batch execution triggered from web interface.")
    ))
    conn.commit()
    
    successful_runs = 0
    executed_results = []
    
    for pid in problem_ids:
        problem = get_problem_db(pid)
        if not problem:
            continue
            
        for prov_key in provider_keys:
            provider = get_provider(prov_key)
            if not provider:
                continue
                
            for cond in conditions:
                exact_prompt = format_prompt(cond, problem["statement"])
                gen_result = provider.generate(problem, cond)
                
                ai_text = gen_result["response_text"]
                status = gen_result["status"]
                
                if status == "success":
                    successful_runs += 1
                    parsed_ans = extract_answer_candidate(ai_text)
                    score, rationale, review = evaluate_final_answer(
                        parsed_ans,
                        problem["final_answer"],
                        problem.get("acceptable_equivalents", [])
                    )
                    step_evals, step_acc = evaluate_steps(ai_text, problem["reference_steps"])
                    errors = classify_errors(ai_text, problem, score, step_evals)
                    
                    init_ans = None
                    verif_effect = 0
                    if cond == "self_verification":
                        init_ans, _, verif_effect = analyze_self_verification(ai_text, problem)
                else:
                    parsed_ans = None
                    score = 0
                    step_acc = 0.0
                    step_evals = []
                    errors = [{
                        "category": "Unverifiable or ambiguous output",
                        "evidence": gen_result.get("error_message", "Provider returned error status"),
                        "severity": "high"
                    }]
                    init_ans = None
                    verif_effect = 0
                    review = True
                    
                res_id = f"res-{uuid.uuid4().hex[:12]}"
                cursor.execute("""
                INSERT INTO experiment_results (
                    id, experiment_id, problem_id, provider, model,
                    prompt_condition, exact_prompt, ai_response, parsed_answer,
                    is_demo, is_correct, step_accuracy, latency_ms, timestamp,
                    status, verification_initial_answer, verification_fixed_error,
                    requires_human_review
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    res_id, exp_id, problem["id"], gen_result["provider"], gen_result["model"],
                    cond, exact_prompt, ai_text, parsed_ans,
                    1 if gen_result.get("is_demo") else 0,
                    score, step_acc, gen_result["latency_ms"], datetime.now().isoformat(),
                    status, init_ans, verif_effect, 1 if review else 0
                ))
                
                for se in step_evals:
                    cursor.execute("""
                    INSERT INTO step_evaluations (
                        result_id, step_number, step_description, status, score, feedback
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        res_id, se["step_number"], se["step_description"],
                        se["status"], se["score"], se["feedback"]
                    ))
                    
                for err in errors:
                    cursor.execute("""
                    INSERT INTO error_classifications (
                        result_id, category, evidence, severity
                    ) VALUES (?, ?, ?, ?)
                    """, (
                        res_id, err["category"], err["evidence"], err["severity"]
                    ))
                    
                executed_results.append({
                    "id": res_id,
                    "problem_id": pid,
                    "provider": gen_result["provider"],
                    "condition": cond,
                    "is_correct": score,
                    "step_accuracy": step_acc,
                    "status": status
                })

    cursor.execute("""
    UPDATE experiments SET status = 'completed', successful_runs = ? WHERE id = ?
    """, (successful_runs, exp_id))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "completed",
        "experiment_id": exp_id,
        "total_runs": total_runs,
        "successful_runs": successful_runs,
        "results": executed_results
    })

@app.route("/api/result/<res_id>")
def api_result_detail(res_id):
    """Fetch result details for modal view."""
    detail = get_result_detail_db(res_id)
    if not detail:
        return jsonify({"error": "Result not found"}), 404
    return jsonify(detail)

@app.route("/api/human-review", methods=["POST"])
def api_submit_human_review():
    """Submit human review override."""
    data = request.get_json() or {}
    res_id = data.get("result_id")
    reviewer = data.get("reviewer_name", "Academic Evaluator").strip()
    corrected_correct = data.get("corrected_is_correct")
    notes = data.get("notes", "").strip()
    
    if not res_id:
        return jsonify({"error": "result_id required"}), 400
        
    conn = get_db()
    cursor = conn.cursor()
    
    # Fetch original score
    row = cursor.execute("SELECT is_correct FROM experiment_results WHERE id = ?", (res_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Result not found"}), 404
    orig_score = row["is_correct"]
    
    cursor.execute("""
    INSERT OR REPLACE INTO human_reviews (
        result_id, reviewer_name, reviewed_at, original_is_correct, corrected_is_correct, notes
    ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        res_id, reviewer, datetime.now().isoformat(), orig_score, corrected_correct, notes
    ))
    cursor.execute("""
    UPDATE experiment_results SET requires_human_review = 0 WHERE id = ?
    """, (res_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Human review recorded."})

@app.route("/api/analytics-data")
def api_analytics_data():
    """Return JSON payload for Chart.js rendering."""
    results = get_all_results_db()
    return jsonify({
        "overall": analytics.compute_overall_metrics(results),
        "by_provider": analytics.compute_by_dimension(results, "provider"),
        "by_topic": analytics.compute_by_dimension(results, "topic"),
        "by_difficulty": analytics.compute_by_dimension(results, "difficulty"),
        "prompt_comp": analytics.compute_prompt_comparison(results),
        "verif": analytics.compute_self_verification_analysis(results),
        "errors": analytics.compute_error_distribution(),
        "heatmap": analytics.compute_heatmap_matrix(results)
    })

# -----------------------------------------------------------------------------
# File Export Routes
# -----------------------------------------------------------------------------

@app.route("/export/xlsx")
def export_xlsx():
    """Download the 10-sheet Excel workbook."""
    filepath = export_service.generate_excel_workbook()
    return send_file(
        filepath,
        as_attachment=True,
        download_name=os.path.basename(filepath),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/export/csv")
def export_csv():
    """Download results as CSV."""
    filepath = export_service.export_results_csv()
    return send_file(
        filepath,
        as_attachment=True,
        download_name=os.path.basename(filepath),
        mimetype="text/csv"
    )

@app.route("/export/problems-csv")
def export_problems_csv():
    """Download problem set as CSV."""
    filepath = export_service.export_problems_csv()
    return send_file(
        filepath,
        as_attachment=True,
        download_name=os.path.basename(filepath),
        mimetype="text/csv"
    )

if __name__ == "__main__":
    port = Config.PORT
    app.run(host="0.0.0.0", port=port, debug=True)
