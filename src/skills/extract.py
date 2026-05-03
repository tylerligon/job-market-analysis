#scans title/decsriptions and returns skill founds for each jobs

import re
import pandas as pd
from skills.skill_dict import SKILLS

def extract_skills_from_text(text: str) -> list[str]:
    if pd.isna(text):
        return []

    text = str(text).lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills

def add_skills_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["skills"] = df["cleaned_description"].apply(extract_skills_from_text)
    return df