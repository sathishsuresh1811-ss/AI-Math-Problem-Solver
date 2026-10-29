"""
Database Module for SQLite persistence.
Manages schema definition, indexing, querying, transactions, and baseline seeding.
"""

import sqlite3
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from config import Config
from math_dataset import PROBLEMS

def get_db():
    """Establish and return SQLite connection with Row factory."""
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(seed_baseline: bool = True):
    """
    Initialize SQLite schema with tables, constraints, and indexes.
    Seeds the 30 problems and baseline benchmark data if empty.
    """
    conn = get_db()
    cursor = conn.cursor()

    # 1. Problems Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        subtopic TEXT,
        difficulty TEXT NOT NULL,
        statement TEXT NOT NULL,
        final_answer TEXT NOT NULL,
        acceptable_equivalents_json TEXT NOT NULL,
        formula TEXT,
        reference_steps_json TEXT NOT NULL,
        common_mistakes_json TEXT,
        verification_status TEXT
    )
    """)

    # 2. Experiments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        created_at TEXT NOT NULL,
        status TEXT NOT NULL,
        total_runs INTEGER DEFAULT 0,
        successful_runs INTEGER DEFAULT 0,
        notes TEXT
    )
    """)

    # 3. Experiment Results Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experiment_results (
        id TEXT PRIMARY KEY,
        experiment_id TEXT,
        problem_id TEXT NOT NULL,
        provider TEXT NOT NULL,
        model TEXT NOT NULL,
        prompt_condition TEXT NOT NULL,
        exact_prompt TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        parsed_answer TEXT,
        is_demo INTEGER DEFAULT 1,
        is_correct INTEGER,
        step_accuracy REAL DEFAULT 0.0,
        latency_ms INTEGER DEFAULT 0,
        timestamp TEXT NOT NULL,
        status TEXT NOT NULL,
        verification_initial_answer TEXT,
        verification_fixed_error INTEGER DEFAULT 0,
        requires_human_review INTEGER DEFAULT 0,
        FOREIGN KEY(problem_id) REFERENCES problems(id),
        FOREIGN KEY(experiment_id) REFERENCES experiments(id) ON DELETE CASCADE
    )
    """)

    # 4. Step Evaluations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS step_evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        result_id TEXT NOT NULL,
        step_number INTEGER NOT NULL,
        step_description TEXT,
        status TEXT NOT NULL,
        score REAL NOT NULL,
        feedback TEXT,
        FOREIGN KEY(result_id) REFERENCES experiment_results(id) ON DELETE CASCADE
    )
    """)

    # 5. Error Classifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS error_classifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        result_id TEXT NOT NULL,
        category TEXT NOT NULL,
        evidence TEXT NOT NULL,
        severity TEXT DEFAULT 'medium',
        is_manual_override INTEGER DEFAULT 0,
        FOREIGN KEY(result_id) REFERENCES experiment_results(id) ON DELETE CASCADE
    )
    """)

    # 6. Human Reviews Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS human_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        result_id TEXT NOT NULL UNIQUE,
        reviewer_name TEXT NOT NULL,
        reviewed_at TEXT NOT NULL,
        original_is_correct INTEGER,
        corrected_is_correct INTEGER,
        notes TEXT,
        FOREIGN KEY(result_id) REFERENCES experiment_results(id) ON DELETE CASCADE
    )
    """)

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_res_problem ON experiment_results(problem_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_res_provider ON experiment_results(provider)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_res_prompt ON experiment_results(prompt_condition)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_res_demo ON experiment_results(is_demo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_err_cat ON error_classifications(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_step_res ON step_evaluations(result_id)")

    conn.commit()

    # Seed problems
    for p in PROBLEMS:
        cursor.execute("""
        INSERT OR REPLACE INTO problems (
            id, topic, subtopic, difficulty, statement, final_answer,
            acceptable_equivalents_json, formula, reference_steps_json,
            common_mistakes_json, verification_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"],
            p["topic"],
            p.get("subtopic", ""),
            p["difficulty"],
            p["statement"],
            p["final_answer"],
            json.dumps(p.get("acceptable_equivalents", [])),
            p.get("formula", ""),
            json.dumps(p.get("reference_steps", [])),
            json.dumps(p.get("common_mistakes", [])),
            p.get("verification_status", "Verified")
        ))
    conn.commit()

    # Check if experiment runs exist; if not and seed_baseline is True, generate baseline benchmark
    cursor.execute("SELECT COUNT(*) as count FROM experiment_results")
    count = cursor.fetchone()["count"]
    if count == 0 and seed_baseline:
        seed_baseline_experiment(conn)

    conn.close()

def seed_baseline_experiment(conn):
    """
    Generate initial baseline benchmark runs across all 30 problems for the 3 conditions.
    Provides immediate rich data for charts, reports, and presentation.
    """
    from ai_providers import LocalDemoSolver
    from prompt_templates import format_prompt
    from answer_checker import extract_answer_candidate, evaluate_final_answer
    from scoring import evaluate_steps, classify_errors, analyze_self_verification

    cursor = conn.cursor()
    exp_id = f"exp-baseline-{int(datetime.now().timestamp())}"
    now_str = datetime.now().isoformat()
    
    cursor.execute("""
    INSERT INTO experiments (id, name, created_at, status, total_runs, successful_runs, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        exp_id,
        "Baseline Benchmark: 30 Problems x 3 Prompt Conditions",
        now_str,
        "completed",
        90,
        90,
        "Standard initial benchmark running the deterministic Local Reference Solver."
    ))

    solver = LocalDemoSolver()
    conditions = ["plain", "step_by_step", "self_verification"]

    for prob in PROBLEMS:
        for cond in conditions:
            exact_prompt = format_prompt(cond, prob["statement"])
            gen_result = solver.generate(prob, cond)
            
            ai_text = gen_result["response_text"]
            parsed_ans = extract_answer_candidate(ai_text)
            
            score, rationale, review = evaluate_final_answer(
                parsed_ans,
                prob["final_answer"],
                prob.get("acceptable_equivalents", [])
            )
            
            step_evals, step_acc = evaluate_steps(ai_text, prob["reference_steps"])
            errors = classify_errors(ai_text, prob, score, step_evals)
            
            init_ans = None
            verif_effect = 0
            if cond == "self_verification":
                init_ans, _, verif_effect = analyze_self_verification(ai_text, prob)
                
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
                res_id, exp_id, prob["id"], gen_result["provider"], gen_result["model"],
                cond, exact_prompt, ai_text, parsed_ans,
                1, score, step_acc, gen_result["latency_ms"], now_str,
                "success", init_ans, verif_effect, 1 if review else 0
            ))
            
            # Step evals
            for se in step_evals:
                cursor.execute("""
                INSERT INTO step_evaluations (
                    result_id, step_number, step_description, status, score, feedback
                ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    res_id, se["step_number"], se["step_description"],
                    se["status"], se["score"], se["feedback"]
                ))
                
            # Errors
            for err in errors:
                cursor.execute("""
                INSERT INTO error_classifications (
                    result_id, category, evidence, severity
                ) VALUES (?, ?, ?, ?)
                """, (
                    res_id, err["category"], err["evidence"], err["severity"]
                ))
                
    conn.commit()

def get_all_problems_db():
    """Retrieve all problems from database."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM problems ORDER BY id ASC").fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["acceptable_equivalents"] = json.loads(d["acceptable_equivalents_json"])
        d["reference_steps"] = json.loads(d["reference_steps_json"])
        d["common_mistakes"] = json.loads(d["common_mistakes_json"]) if d["common_mistakes_json"] else []
        result.append(d)
    return result

def get_problem_db(prob_id: str):
    """Retrieve single problem from database."""
    conn = get_db()
    r = conn.execute("SELECT * FROM problems WHERE id = ?", (prob_id.upper(),)).fetchone()
    conn.close()
    if not r:
        return None
    d = dict(r)
    d["acceptable_equivalents"] = json.loads(d["acceptable_equivalents_json"])
    d["reference_steps"] = json.loads(d["reference_steps_json"])
    d["common_mistakes"] = json.loads(d["common_mistakes_json"]) if d["common_mistakes_json"] else []
    return d

def get_all_results_db(filters: Optional[Dict[str, Any]] = None):
    """Query experiment results with optional filters."""
    conn = get_db()
    query = """
    SELECT r.*, p.topic, p.difficulty, p.statement, p.final_answer as reference_answer,
           hr.reviewer_name, hr.corrected_is_correct, hr.notes as review_notes
    FROM experiment_results r
    JOIN problems p ON r.problem_id = p.id
    LEFT JOIN human_reviews hr ON r.id = hr.result_id
    WHERE 1=1
    """
    params = []
    if filters:
        if filters.get("topic"):
            query += " AND p.topic = ?"
            params.append(filters["topic"])
        if filters.get("difficulty"):
            query += " AND p.difficulty = ?"
            params.append(filters["difficulty"])
        if filters.get("provider"):
            query += " AND r.provider LIKE ?"
            params.append(f"%{filters['provider']}%")
        if filters.get("prompt_condition"):
            query += " AND r.prompt_condition = ?"
            params.append(filters["prompt_condition"])
        if filters.get("is_demo") is not None:
            query += " AND r.is_demo = ?"
            params.append(int(filters["is_demo"]))
        if filters.get("is_correct") is not None:
            query += " AND r.is_correct = ?"
            params.append(int(filters["is_correct"]))
        if filters.get("search"):
            query += " AND (p.statement LIKE ? OR r.parsed_answer LIKE ? OR r.problem_id LIKE ?)"
            s = f"%{filters['search']}%"
            params.extend([s, s, s])

    query += " ORDER BY r.timestamp DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_result_detail_db(result_id: str):
    """Retrieve full details for a result including step evals, errors, and reviews."""
    conn = get_db()
    res_row = conn.execute("""
    SELECT r.*, p.topic, p.subtopic, p.difficulty, p.statement, p.final_answer as reference_answer,
           p.formula, p.reference_steps_json, p.common_mistakes_json,
           hr.reviewer_name, hr.reviewed_at, hr.corrected_is_correct, hr.notes as review_notes
    FROM experiment_results r
    JOIN problems p ON r.problem_id = p.id
    LEFT JOIN human_reviews hr ON r.id = hr.result_id
    WHERE r.id = ?
    """, (result_id,)).fetchone()
    
    if not res_row:
        conn.close()
        return None
        
    result_data = dict(res_row)
    result_data["reference_steps"] = json.loads(result_data["reference_steps_json"])
    result_data["common_mistakes"] = json.loads(result_data["common_mistakes_json"]) if result_data["common_mistakes_json"] else []
    
    step_rows = conn.execute("""
    SELECT * FROM step_evaluations WHERE result_id = ? ORDER BY step_number ASC
    """, (result_id,)).fetchall()
    result_data["step_evaluations"] = [dict(s) for s in step_rows]
    
    err_rows = conn.execute("""
    SELECT * FROM error_classifications WHERE result_id = ?
    """, (result_id,)).fetchall()
    result_data["error_classifications"] = [dict(e) for e in err_rows]
    
    conn.close()
    return result_data
