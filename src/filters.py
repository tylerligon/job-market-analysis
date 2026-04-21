import pandas as pd
import re

# early career keywords
EARLY_CAREER_TERMS = [
    "intern", "internship", "entry level", "new grad", "graduate",
    "junior", "associate", "apprentice"
]

# keywords that don't imdicate early career
EXCLUDE_TERMS = [
    "senior", "staff", "principal", "lead", "manager", "director", "vp"
]

# keywords that indicate tech-related jobs
TECH_TERMS = [
    "software", "data", "machine learning", "ai", "developer", "engineer",
    "analyst", "cloud", "cybersecurity", "product", "frontend", "backend",
    "full stack", "devops", "python", "sql", "java", "javascript"
]

# covert values into a clean lowercase string and prevent any errors if the value is missing or not a text
def safe_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip().lower()

# combines multiple columns into one text field to allow for easy searching
def combine_text(row):
    title = safe_text(row.get("title", ""))
    description = safe_text(row.get("description", ""))
    company = safe_text(row.get("company", ""))
    location = safe_text(row.get("location", ""))

    return f"{title} {description} {company} {location}"


def contains_any(text, terms):
    return any(term in text for term in terms)

# checks for keywords matching in the list of early career keywords
def is_early_career(text):
    return contains_any(text, EARLY_CAREER_TERMS)

# checks for keywords matching in the list of excluding keywords
def is_not_senior(text):
    return not contains_any(text, EXCLUDE_TERMS)

# checks for keywords matching in the list of tech related keywords
def is_tech_role(text):
    return contains_any(text, TECH_TERMS)

# main filtering
def filter_jobs(df):
    df = df.copy() # keep a copy to not tamper with original dataset

    # Normalize likely columns
    expected_cols = ["title", "description", "company", "location"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    # remove duplicate rows
    df = df.drop_duplicates()

    # remove rows with missing titles or description
    df = df.dropna(subset=["title", "description"], how="any")

    # combine into one searchable field
    df["combined_text"] = df.apply(combine_text, axis=1)

    # filters applied
    df = df[
        df["combined_text"].apply(is_early_career) &
        df["combined_text"].apply(is_not_senior) &
        df["combined_text"].apply(is_tech_role)
    ]

    # reset index after filtering
    return df.reset_index(drop=True)
