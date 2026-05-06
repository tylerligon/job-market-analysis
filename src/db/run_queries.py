import os
import pandas as pd

from db.connection import get_connection


QUERIES = {
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
    "avg_salary_by_role": """
        SELECT role_type, ROUND(AVG(mean_salary)::numeric, 2) AS avg_salary
        FROM jobs
        WHERE mean_salary IS NOT NULL
        GROUP BY role_type
        ORDER BY avg_salary DESC;
    """
}


def run_analysis_queries(output_dir: str = "output/tables") -> None:
    os.makedirs(output_dir, exist_ok=True)

    with get_connection() as conn:
        for name, query in QUERIES.items():
            df = pd.read_sql(query, conn)
            out_path = f"{output_dir}/{name}.csv"
            df.to_csv(out_path, index=False)
            print(f"Saved {out_path}")