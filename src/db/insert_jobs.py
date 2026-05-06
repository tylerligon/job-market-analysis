###insert jobs into db
import ast
from typing import Any

import pandas as pd

from db.connection import get_connection


JOB_DB_COLUMNS = [
    "job_id",
    "title",
    "company",
    "location",
    "site",
    "job_type",
    "date_posted",
    "is_remote",
    "min_amount",
    "max_amount",
    "mean_salary",
    "interval",
    "currency",
    "role_type",
    "description",
    "cleaned_description",
]


def _nullify(value: Any):
    if pd.isna(value):
        return None
    return value


def _parse_skills(value) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return sorted({
            str(skill).strip().lower()
            for skill in value
            if str(skill).strip()
        })

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []

        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list):
                return sorted({
                    str(skill).strip().lower()
                    for skill in parsed
                    if str(skill).strip()
                })
        except (ValueError, SyntaxError):
            pass

        return sorted({
            skill.strip().lower()
            for skill in text.split(",")
            if skill.strip()
        })

    if pd.isna(value):
        return []

    return []


def _prepare_job_records(df: pd.DataFrame) -> list[tuple]:
    required_cols = [
        "id",
        "title",
        "company",
        "location",
        "site",
        "job_type",
        "date_posted",
        "is_remote",
        "min_amount",
        "max_amount",
        "mean_salary",
        "interval",
        "currency",
        "description",
        "cleaned_description",
    ]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {missing}")

    records = []

    for _, row in df.iterrows():
        job_id = str(row["id"]).strip()
        if not job_id:
            continue

        date_posted = _nullify(row.get("date_posted"))
        if date_posted == "":
            date_posted = None

        is_remote = _nullify(row.get("is_remote"))
        if is_remote is not None:
            is_remote = bool(is_remote)

        record = (
            job_id,
            _nullify(row.get("title")),
            _nullify(row.get("company")),
            _nullify(row.get("location")),
            _nullify(row.get("site")),
            _nullify(row.get("job_type")),
            date_posted,
            is_remote,
            _nullify(row.get("min_amount")),
            _nullify(row.get("max_amount")),
            _nullify(row.get("mean_salary")),
            _nullify(row.get("interval")),
            _nullify(row.get("currency")),
            _nullify(row.get("role_type")) if "role_type" in df.columns else None,
            _nullify(row.get("description")),
            _nullify(row.get("cleaned_description")),
        )
        records.append(record)

    return records


def insert_jobs(df: pd.DataFrame) -> None:
    if "skills" not in df.columns:
        raise ValueError("DataFrame must contain a 'skills' column.")

    job_records = _prepare_job_records(df)

    unique_skills = sorted(
        {
            skill
            for skills_value in df["skills"]
            for skill in _parse_skills(skills_value)
        }
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO jobs (
                    job_id, title, company, location, site, job_type, date_posted,
                    is_remote, min_amount, max_amount, mean_salary, interval,
                    currency, role_type, description, cleaned_description
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                ON CONFLICT (job_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    company = EXCLUDED.company,
                    location = EXCLUDED.location,
                    site = EXCLUDED.site,
                    job_type = EXCLUDED.job_type,
                    date_posted = EXCLUDED.date_posted,
                    is_remote = EXCLUDED.is_remote,
                    min_amount = EXCLUDED.min_amount,
                    max_amount = EXCLUDED.max_amount,
                    mean_salary = EXCLUDED.mean_salary,
                    interval = EXCLUDED.interval,
                    currency = EXCLUDED.currency,
                    role_type = EXCLUDED.role_type,
                    description = EXCLUDED.description,
                    cleaned_description = EXCLUDED.cleaned_description
                """,
                job_records,
            )

            cur.executemany(
                """
                INSERT INTO skills (skill_name)
                VALUES (%s)
                ON CONFLICT (skill_name) DO NOTHING
                """,
                [(skill,) for skill in unique_skills],
            )

            cur.execute(
                "SELECT skill_id, skill_name FROM skills"
            )
            skill_map = {skill_name: skill_id for skill_id, skill_name in cur.fetchall()}

            job_skill_records = []
            for _, row in df.iterrows():
                job_id = str(row["id"]).strip()
                if not job_id:
                    continue

                for skill in _parse_skills(row["skills"]):
                    skill_id = skill_map.get(skill)
                    if skill_id is not None:
                        job_skill_records.append((job_id, skill_id))

            cur.executemany(
                """
                INSERT INTO job_skills (job_id, skill_id)
                VALUES (%s, %s)
                ON CONFLICT (job_id, skill_id) DO NOTHING
                """,
                job_skill_records,
            )

        conn.commit()

    print("Jobs, skills, and job-skill relationships inserted successfully.")


if __name__ == "__main__":
    df = pd.read_csv("data/processed/cleaned_jobs_with_skills.csv")
    insert_jobs(df)