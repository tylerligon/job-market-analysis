#compare skills patterns by role type, like SWE vs data sci, vs cybersecurityimport re
from collections import Counter

import pandas as pd
import re

ROLE_PATTERNS = {
    "software": [
        r"\bsoftware engineer\b",
        r"\bsoftware developer\b",
        r"\bdeveloper\b",
        r"\bbackend\b",
        r"\bback-end\b",
        r"\bfrontend\b",
        r"\bfront-end\b",
        r"\bfull stack\b",
        r"\bfull-stack\b",
        r"\bweb developer\b",
        r"\bsdet\b",
    ],
    "data": [
        r"\bdata scientist\b",
        r"\bdata science\b",
        r"\bdata analyst\b",
        r"\bdata engineer\b",
        r"\bbusiness intelligence\b",
        r"\bmachine learning\b",
        r"\bai\b",
        r"\bml\b",
        r"\banalytics\b",
    ],
    "cybersecurity": [
        r"\bcyber\b",
        r"\bcybersecurity\b",
        r"\binformation security\b",
        r"\bsecurity analyst\b",
        r"\bsecurity engineer\b",
        r"\bsecurity\b",
        r"\bsoc\b",
        r"\biam\b",
        r"\bincident response\b",
        r"\bthreat\b",
        r"\bvulnerability\b",
    ],
    "devops_cloud": [
        r"\bdevops\b",
        r"\bsite reliability\b",
        r"\bsre\b",
        r"\bcloud\b",
        r"\bplatform engineer\b",
        r"\binfrastructure\b",
        r"\bnetwork engineer\b",
        r"\bsystems engineer\b",
    ],
    "it_support": [
        r"\bit\b",
        r"\binformation technology\b",
        r"\bhelp desk\b",
        r"\btechnical support\b",
        r"\bsupport analyst\b",
        r"\bsystems administrator\b",
        r"\bsecurity specialist\b",
    ],
}


def classify_role_type(title: str) -> str:
    """
    Classify a job title into a broad role type bucket.
    Returns 'other' if no pattern matches.
    """
    if pd.isna(title):
        return "other"

    title = str(title).lower().strip()

    for role_type, patterns in ROLE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, title):
                return role_type

    return "other"


def add_role_type_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a role_type column based on the job title.
    """
    df = df.copy()

    if "title" not in df.columns:
        df["role_type"] = "other"
        return df

    df["role_type"] = df["title"].apply(classify_role_type)
    return df


def role_type_counts(df: pd.DataFrame) -> pd.Series:
    """
    Return counts of jobs by role type.
    """
    if "role_type" not in df.columns:
        df = add_role_type_column(df)

    return df["role_type"].value_counts()


def top_skills_by_role_type(df: pd.DataFrame, top_n: int = 10) -> dict[str, list[tuple[str, int]]]:
    """
    Return the top N skills for each role type.

    Expects:
    - df['role_type']
    - df['skills'] where each row is a list of skills
    """
    if "role_type" not in df.columns:
        df = add_role_type_column(df)

    results = {}

    for role_type in df["role_type"].dropna().unique():
        counter = Counter()
        role_df = df[df["role_type"] == role_type]

        for skills in role_df["skills"]:
            if isinstance(skills, list):
                counter.update(skills)

        results[role_type] = counter.most_common(top_n)

    return results


def role_type_summary_table(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Build a flat summary table with columns:
    role_type, skill, count
    """
    skill_map = top_skills_by_role_type(df, top_n=top_n)

    rows = []
    for role_type, skill_counts in skill_map.items():
        for skill, count in skill_counts:
            rows.append({
                "role_type": role_type,
                "skill": skill,
                "count": count,
            })

    return pd.DataFrame(rows)