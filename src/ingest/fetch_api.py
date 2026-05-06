"""
fetch_api.py — Pull early-career job listings from the JSearch API (RapidAPI).

Set JSEARCH_API_KEY as an environment variable (your RapidAPI key).
Docs: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
"""

import os
import time
import logging
import requests
import pandas as pd

JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"

ENTRY_QUERIES = [
    "software engineer intern",
    "data science intern",
    "entry level software developer",
    "new grad software engineer",
    "junior data analyst",
    "cybersecurity intern",
    "machine learning intern",
    "frontend developer entry level",
    "backend developer new grad",
    "devops intern",
]

# Columns the rest of the pipeline expects (matches Kaggle schema)
EXPECTED_COLS = [
    "id", "site", "job_url", "job_url_direct", "title", "company",
    "location", "job_type", "date_posted", "is_remote",
    "min_amount", "max_amount", "mean_salary", "interval",
    "currency", "job_level", "job_function", "company_industry",
    "company_num_employees", "company_revenue",
    "description", "cleaned_description",
]


def _get_headers() -> dict:
    api_key = os.getenv("JSEARCH_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "JSEARCH_API_KEY environment variable not set. "
            "Get your key at https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch"
        )
    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }


def _safe_float(val) -> float | None:
    """Convert a value to float safely — returns None on any failure."""  # fix: None-safe salary
    try:
        return float(val) if val is not None else None
    except (ValueError, TypeError):
        return None


def _fetch_one_query(query: str, num_pages: int = 3) -> list[dict]:
    """Fetch up to num_pages of results for a single search query."""
    headers = _get_headers()
    results = []

    for page in range(1, num_pages + 1):
        params = {
            "query": query,
            "page": str(page),
            "num_pages": "1",
            "date_posted": "month",
            "employment_types": "INTERN,FULLTIME",
        }
        try:
            resp = requests.get(
                JSEARCH_URL, headers=headers, params=params, timeout=15
            )
            resp.raise_for_status()
            jobs = resp.json().get("data", [])
            results.extend(jobs)
            logging.info(f"  [{query}] page {page}: {len(jobs)} jobs")
            if not jobs:
                break
            time.sleep(0.5)
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            if status_code == 429:
                raise

            logging.warning(f"  [{query}] page {page} failed: {e}")
            break
        except requests.RequestException as e:
            logging.warning(f"  [{query}] page {page} failed: {e}")
            break

    return results


def _normalize_jsearch_job(job: dict) -> dict:
    """Map a JSearch job dict to the Kaggle column schema."""
    s_min = _safe_float(job.get("job_min_salary"))    # fix: use _safe_float
    s_max = _safe_float(job.get("job_max_salary"))    # fix: use _safe_float
    mean_salary = (s_min + s_max) / 2 if s_min is not None and s_max is not None else None

    raw_desc = job.get("job_description") or ""        # fix: 'or ""' guards explicit None
    posted = job.get("job_posted_at_datetime_utc") or ""

    location_parts = [
        job.get("job_city"),
        job.get("job_state"),
        job.get("job_country")
    ]
    location = ", ".join([part for part in location_parts if part])

    return {
        "id":                   job.get("job_id", ""),
        "site":                 "jsearch",
        "job_url":              job.get("job_apply_link", ""),
        "job_url_direct":       job.get("job_apply_link", ""),
        "title":                job.get("job_title", ""),
        "company":              job.get("employer_name", ""),
        "location":             location,
        "job_type":             (job.get("job_employment_type") or "").lower(),
        "date_posted":          posted[:10] if posted else None,
        "is_remote":            bool(job.get("job_is_remote", False)),
        "min_amount":           s_min,
        "max_amount":           s_max,
        "mean_salary":          mean_salary,
        "interval":             (job.get("job_salary_period") or "yearly").lower(),
        "currency":             job.get("job_salary_currency", "USD"),
        "job_level":            None,
        "job_function":         None,
        "company_industry":     job.get("employer_company_type"),
        "company_num_employees": None,
        "company_revenue":      None,
        "description":          raw_desc,
        "cleaned_description":  raw_desc.lower(),         # fix: uses guarded raw_desc
    }


def fetch_jsearch_jobs(
    queries: list[str] = None,
    num_pages: int = 3,
) -> pd.DataFrame:
    """
    Fetch jobs from JSearch for each query string.

    Args:
        queries:   List of search strings. Defaults to ENTRY_QUERIES.
        num_pages: Pages per query (10 results/page on free tier).

    Returns:
        DataFrame with the same columns as the Kaggle cleaned data,
        ready to pass into merge_sources().
    """
    if queries is None:
        queries = ENTRY_QUERIES

    all_jobs = []
    for q in queries:
        logging.info(f"Fetching JSearch query: '{q}'")
        try:
            all_jobs.extend(_fetch_one_query(q, num_pages=num_pages))
        except requests.HTTPError as e:
            logging.warning(f"Rate limited by JSearch API, stopping api fetch: {e}")
            break

    if not all_jobs:
        logging.warning("No jobs fetched from JSearch API.")
        return pd.DataFrame(columns=EXPECTED_COLS)  # fix: return typed empty df

    df = pd.DataFrame([_normalize_jsearch_job(j) for j in all_jobs])
    df = df.drop_duplicates(subset=["id"])

    # Ensure all expected columns exist even if API omitted them
    for col in EXPECTED_COLS:                        # fix: column alignment guard
        if col not in df.columns:
            df[col] = None

    logging.info(f"JSearch fetch complete: {len(df)} unique jobs")
    return df #fetch JSEARCH API in here

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    df = fetch_jsearch_jobs(num_pages=1)
    print(df.head())
    print("Shape:", df.shape)

    df.to_csv("data/processed/api_jobs_cleaned.csv", index=False)