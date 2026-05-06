from db.connection import get_connection

def reset_tables():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE job_skills, skills, jobs RESTART IDENTITY CASCADE;")
        conn.commit()

    print("Tables reset successfully.")