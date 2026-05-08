import os
import pandas as pd

from db.connection import get_connection


QUERIES = {
    "total_jobs": """
        SELECT COUNT(*) AS total_jobs
        FROM jobs;
    """,
    "role_type_counts": """
        SELECT role_type, COUNT(*) AS count
        FROM jobs
        GROUP BY role_type
        ORDER BY count DESC;
    """,
    "top_skills": """
        SELECT s.skill_name, COUNT(*) AS count
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.skill_id
        GROUP BY s.skill_name
        ORDER BY count DESC
        LIMIT 20;
    """,
    "top_companies": """
        SELECT company, COUNT(*) AS count
        FROM jobs
        GROUP BY company
        ORDER BY count DESC
        LIMIT 20;
    """,
    "remote_vs_non_remote": """
        SELECT is_remote, COUNT(*) AS count
        FROM jobs
        GROUP BY is_remote
        ORDER BY count DESC;
    """,
    "avg_salary_by_role": """
        SELECT role_type, ROUND(AVG(mean_salary)::numeric, 2) AS avg_salary
        FROM jobs
        WHERE mean_salary IS NOT NULL
        GROUP BY role_type
        ORDER BY avg_salary DESC;
    """,
    "top_companies_by_avg_salary": """
        SELECT company, ROUND(AVG(mean_salary)::numeric, 2) AS avg_salary, COUNT(*) AS job_count
        FROM jobs
        WHERE mean_salary IS NOT NULL
        GROUP BY company
        HAVING COUNT(*) >= 3
        ORDER BY avg_salary DESC
        LIMIT 10;
    """,
    "top_remote_role_types": """
        SELECT role_type, COUNT(*) AS remote_count
        FROM jobs
        WHERE is_remote = TRUE
        GROUP BY role_type
        ORDER BY remote_count DESC;
    """,
    "top_skills_software": """
        SELECT s.skill_name, COUNT(*) AS count
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.skill_id
        JOIN jobs j ON js.job_id = j.job_id
        WHERE j.role_type = 'software'
        GROUP BY s.skill_name
        ORDER BY count DESC
        LIMIT 10;
    """,
    "top_skills_data": """
        SELECT s.skill_name, COUNT(*) AS count
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.skill_id
        JOIN jobs j ON js.job_id = j.job_id
        WHERE j.role_type = 'data'
        GROUP BY s.skill_name
        ORDER BY count DESC
        LIMIT 10;
    """,
    "top_skills_cybersecurity": """
        SELECT s.skill_name, COUNT(*) AS count
        FROM job_skills js
        JOIN skills s ON js.skill_id = s.skill_id
        JOIN jobs j ON js.job_id = j.job_id
        WHERE j.role_type = 'cybersecurity'
        GROUP BY s.skill_name
        ORDER BY count DESC
        LIMIT 10;
    """,
}


def run_query_to_df(conn, query: str) -> pd.DataFrame:
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)


def run_analysis_queries(output_dir: str = "output/tables") -> None:
    os.makedirs(output_dir, exist_ok=True)

    with get_connection() as conn:
        for name, query in QUERIES.items():
            df = run_query_to_df(conn, query)
            out_path = f"{output_dir}/{name}.csv"
            df.to_csv(out_path, index=False)
            print(f"Saved {out_path}")