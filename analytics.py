"""
Analytics Module for AI Math Problem Explainer and Error Checker.
Aggregates performance metrics, prompt condition deltas, before/after self-verification,
error category distributions, and heatmap coverage.
"""

from typing import Dict, List, Any
from database import get_all_results_db, get_db

def compute_overall_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute top-level summary metrics."""
    if not results:
        return {
            "total_runs": 0,
            "live_runs": 0,
            "demo_runs": 0,
            "final_accuracy": 0.0,
            "mean_step_accuracy": 0.0,
            "correct_count": 0,
            "incorrect_count": 0,
            "unscorable_count": 0,
            "needs_review_count": 0,
            "mean_latency_ms": 0
        }

    total = len(results)
    live = sum(1 for r in results if r.get("is_demo") == 0)
    demo = sum(1 for r in results if r.get("is_demo") == 1)
    
    # Consider human overrides if present
    def is_run_correct(r):
        if r.get("corrected_is_correct") is not None:
            return r.get("corrected_is_correct")
        return r.get("is_correct")

    correct = sum(1 for r in results if is_run_correct(r) == 1)
    incorrect = sum(1 for r in results if is_run_correct(r) == 0)
    unscorable = sum(1 for r in results if is_run_correct(r) == -1)
    needs_review = sum(1 for r in results if r.get("requires_human_review") == 1)

    scorable_total = correct + incorrect
    final_accuracy = round((correct / scorable_total * 100.0), 2) if scorable_total > 0 else 0.0
    
    step_scores = [r.get("step_accuracy", 0.0) for r in results if r.get("step_accuracy") is not None]
    mean_step = round(sum(step_scores) / len(step_scores), 2) if step_scores else 0.0
    
    latencies = [r.get("latency_ms", 0) for r in results if r.get("latency_ms")]
    mean_lat = round(sum(latencies) / len(latencies), 0) if latencies else 0

    return {
        "total_runs": total,
        "live_runs": live,
        "demo_runs": demo,
        "final_accuracy": final_accuracy,
        "mean_step_accuracy": mean_step,
        "correct_count": correct,
        "incorrect_count": incorrect,
        "unscorable_count": unscorable,
        "needs_review_count": needs_review,
        "mean_latency_ms": int(mean_lat)
    }

def compute_by_dimension(results: List[Dict[str, Any]], dimension_key: str) -> List[Dict[str, Any]]:
    """Group results by a specific dimension (provider, topic, difficulty, prompt_condition)."""
    if not results:
        return []

    groups = {}
    for r in results:
        val = r.get(dimension_key, "Unknown")
        if val not in groups:
            groups[val] = []
        groups[val].append(r)

    summary = []
    for group_name, items in groups.items():
        metrics = compute_overall_metrics(items)
        summary.append({
            "dimension": dimension_key,
            "label": group_name,
            "total_runs": metrics["total_runs"],
            "live_runs": metrics["live_runs"],
            "demo_runs": metrics["demo_runs"],
            "final_accuracy": metrics["final_accuracy"],
            "mean_step_accuracy": metrics["mean_step_accuracy"],
            "correct_count": metrics["correct_count"],
            "incorrect_count": metrics["incorrect_count"],
            "mean_latency_ms": metrics["mean_latency_ms"]
        })

    # Sort descending by total runs
    summary.sort(key=lambda x: x["total_runs"], reverse=True)
    return summary

def compute_prompt_comparison(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compare performance across the 3 prompt conditions: plain, step_by_step, self_verification."""
    plain_runs = [r for r in results if r.get("prompt_condition") == "plain"]
    step_runs = [r for r in results if r.get("prompt_condition") == "step_by_step"]
    verif_runs = [r for r in results if r.get("prompt_condition") == "self_verification"]

    plain_metrics = compute_overall_metrics(plain_runs)
    step_metrics = compute_overall_metrics(step_runs)
    verif_metrics = compute_overall_metrics(verif_runs)

    # Percentage point differences
    step_vs_plain_acc_delta = round(step_metrics["final_accuracy"] - plain_metrics["final_accuracy"], 2)
    step_vs_plain_step_delta = round(step_metrics["mean_step_accuracy"] - plain_metrics["mean_step_accuracy"], 2)
    
    verif_vs_plain_acc_delta = round(verif_metrics["final_accuracy"] - plain_metrics["final_accuracy"], 2)
    verif_vs_step_acc_delta = round(verif_metrics["final_accuracy"] - step_metrics["final_accuracy"], 2)

    return {
        "plain": plain_metrics,
        "step_by_step": step_metrics,
        "self_verification": verif_metrics,
        "deltas": {
            "step_vs_plain_accuracy_pp": step_vs_plain_acc_delta,
            "step_vs_plain_step_pp": step_vs_plain_step_delta,
            "verif_vs_plain_accuracy_pp": verif_vs_plain_acc_delta,
            "verif_vs_step_accuracy_pp": verif_vs_step_acc_delta
        }
    }

def compute_self_verification_analysis(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detailed before/after verification analysis:
    - Cases where verification fixed an error
    - Cases where verification introduced a new error
    - Cases where accuracy was unchanged
    - Percentage point changes and relative percent improvements
    """
    verif_results = [r for r in results if r.get("prompt_condition") == "self_verification"]
    
    fixed_count = sum(1 for r in verif_results if r.get("verification_fixed_error") == 1)
    introduced_count = sum(1 for r in verif_results if r.get("verification_fixed_error") == -1)
    unchanged_count = sum(1 for r in verif_results if r.get("verification_fixed_error") == 0)
    
    total = len(verif_results)
    
    # Calculate pre-verification vs post-verification accuracy on these runs
    # If verification_fixed_error == 1, initial was 0, final was 1
    # If verification_fixed_error == -1, initial was 1, final was 0
    # If verification_fixed_error == 0, initial was same as final
    pre_correct = 0
    post_correct = 0
    
    for r in verif_results:
        final_c = 1 if r.get("is_correct") == 1 else 0
        effect = r.get("verification_fixed_error", 0)
        if effect == 1:
            init_c = 0
        elif effect == -1:
            init_c = 1
        else:
            init_c = final_c
            
        pre_correct += init_c
        post_correct += final_c
        
    pre_acc = round((pre_correct / total * 100.0), 2) if total > 0 else 0.0
    post_acc = round((post_correct / total * 100.0), 2) if total > 0 else 0.0
    
    pp_change = round(post_acc - pre_acc, 2)
    relative_pct_improvement = round(((post_acc - pre_acc) / pre_acc * 100.0), 2) if pre_acc > 0 else 0.0

    # Topic breakdown for verification effect
    topic_breakdown = {}
    for r in verif_results:
        t = r.get("topic", "Other")
        if t not in topic_breakdown:
            topic_breakdown[t] = {"total": 0, "fixed": 0, "introduced": 0, "unchanged": 0}
        topic_breakdown[t]["total"] += 1
        if r.get("verification_fixed_error") == 1:
            topic_breakdown[t]["fixed"] += 1
        elif r.get("verification_fixed_error") == -1:
            topic_breakdown[t]["introduced"] += 1
        else:
            topic_breakdown[t]["unchanged"] += 1

    return {
        "total_verification_runs": total,
        "fixed_count": fixed_count,
        "introduced_count": introduced_count,
        "unchanged_count": unchanged_count,
        "pre_verification_accuracy": pre_acc,
        "post_verification_accuracy": post_acc,
        "percentage_point_change": pp_change,
        "relative_pct_improvement": relative_pct_improvement,
        "topic_breakdown": topic_breakdown
    }

def compute_error_distribution() -> List[Dict[str, Any]]:
    """Query error classifications grouped by category."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT category, COUNT(*) as count,
           SUM(CASE WHEN severity = 'high' THEN 1 ELSE 0 END) as high_count,
           SUM(CASE WHEN severity = 'medium' THEN 1 ELSE 0 END) as medium_count,
           SUM(CASE WHEN severity = 'low' THEN 1 ELSE 0 END) as low_count
    FROM error_classifications
    GROUP BY category
    ORDER BY count DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def compute_heatmap_matrix(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate problem x condition heatmap data matrix."""
    if not results:
        return {"problems": [], "columns": [], "matrix": {}}

    problems = sorted(list({r["problem_id"] for r in results}))
    conditions = ["plain", "step_by_step", "self_verification"]
    
    matrix = {}
    for pid in problems:
        matrix[pid] = {}
        for c in conditions:
            # Find latest run for this problem and condition
            matching = [r for r in results if r["problem_id"] == pid and r["prompt_condition"] == c]
            if matching:
                latest = matching[0]
                matrix[pid][c] = {
                    "is_correct": latest.get("is_correct"),
                    "step_accuracy": latest.get("step_accuracy", 0.0),
                    "is_demo": latest.get("is_demo", 1),
                    "result_id": latest.get("id")
                }
            else:
                matrix[pid][c] = None

    return {
        "problems": problems,
        "columns": conditions,
        "matrix": matrix
    }
