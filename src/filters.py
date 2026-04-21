import pandas as pd
import re

EARLY_CAREER_TERMS = [
    "intern", "internship", "entry level", "new grad", "graduate",
    "junior", "associate", "apprentice"
]

EXCLUDE_TERMS = [
    "senior", "staff", "principal", "lead", "manager", "director", "vp"
]

TECH_TERMS = [
    "software", "data", "machine learning", "ai", "developer", "engineer",
    "analyst", "cloud", "cybersecurity", "product", "frontend", "backend",
    "full stack", "devops", "python", "sql", "java", "javascript"
]

def safe_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()

def combine_text(row):
    title = safe_text(row.get("title", ""))
    description = safe_text(row.get("description", ""))
    company = safe_text(row.get("company", ""))
    location = safe_text(row.get("location", ""))
    return f"{title} {description} {company} {location}"

def contains_any(text, terms):
    return any(term in text for term in terms)

def is_early_career(text):
    return contains_any(text, EARLY_CAREER_TERMS)

def is_not_senior(text):
    return not contains_any(text, EXCLUDE_TERMS)

def is_tech_role(text):
    return contains_any(text, TECH_TERMS)

def filter_jobs(df):
    df = df.copy()

    # Normalize likely columns
    expected_cols = ["title", "description", "company", "location"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    df = df.drop_duplicates()
    df = df.dropna(subset=["title", "description"], how="any")

    df["combined_text"] = df.apply(combine_text, axis=1)

    df = df[
        df["combined_text"].apply(is_early_career) &
        df["combined_text"].apply(is_not_senior) &
        df["combined_text"].apply(is_tech_role)
    ]

    return df.reset_index(drop=True)
