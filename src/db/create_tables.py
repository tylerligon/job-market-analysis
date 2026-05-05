##create tables for db
from pathlib import Path

from src.db.connection import get_connection


def create_tables(schema_path: str = "sql/schema.sql") -> None:
    project_root = Path(__file__).resolve().parents[2]
    full_schema_path = project_root / schema_path

    if not full_schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {full_schema_path}")

    schema_sql = full_schema_path.read_text(encoding="utf-8")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()

    print("Tables created successfully.")


if __name__ == "__main__":
    create_tables()