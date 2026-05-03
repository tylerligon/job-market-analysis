#filters for entry-level, internship, junior, newgrad tech roles

import pandas as pd

ENTRY_PATTERNS = [
    r"\bintern\b",
    r"\binternship\b",
    r"\bentry level\b",
    r"\bnew grad\b",
    r"\bjunior\b",
    r"\bjr\.?\b",
    r"\banalyst i\b",
    r"\bengineer i\b",
    r"\bdeveloper i\b",
    r"\bscientist i\b",
    r"\blevel 1\b",
]

TECH_TITLE_PATTERNS = [
    r"\bsoftware engineer\b",
    r"\bsoftware developer\b",
    r"\bsoftware engineering\b",
    r"\bdata scientist\b",
    r"\bdata science\b",
    r"\bdata analyst\b",
    r"\bdata engineer\b",
    r"\bmachine learning\b",
    r"\bai\b",
    r"\bml\b",
    r"\bcyber\b",
    r"\bcybersecurity\b",
    r"\binformation security\b",
    r"\bsecurity engineer\b",
    r"\bsecurity analyst\b",
    r"\bnetwork engineer\b",
    r"\bweb developer\b",
    r"\bfront-end\b",
    r"\bfrontend\b",
    r"\bback-end\b",
    r"\bbackend\b",
    r"\bfull stack\b",
    r"\bdevops\b",
    r"\bsite reliability\b",
    r"\bsre\b",
    r"\bit security\b",
    r"\bit intern\b",
    r"\binformation technology\b",
]

EXCLUDE_PATTERNS = [
    r"\bsenior\b",
    r"\bsr\.?\b",
    r"\bprincipal\b",
    r"\bstaff\b",
    r"\blead\b",
    r"\bmanager\b",
    r"\bdirector\b",
    r"\bhead\b",
    r"\bvice president\b",
    r"\bvp\b",
    r"\barchitect\b",
    r"\bconsultant\b",
    r"\bexpert-level\b",
    r"\bii\b",
    r"\biii\b",
    r"\biv\b",
    r"\bprocess engineer\b",
    r"\btransmission engineer\b",
    r"\bcivil engineer\b",
    r"\bmechanical engineer\b",
    r"\belectrical engineer\b",
    r"\bmanufacturing\b",
    r"\bphotolithography\b",
    r"\bmask design\b",
    r"\benergy settlement\b",
    r"\bauditor\b",
]

def filter_roles(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "title" not in df.columns:
        return df

    titles = df["title"].fillna("").str.lower().str.strip()

    entry_mask = titles.str.contains("|".join(ENTRY_PATTERNS), regex=True, na=False)
    tech_mask = titles.str.contains("|".join(TECH_TITLE_PATTERNS), regex=True, na=False)
    exclude_mask = titles.str.contains("|".join(EXCLUDE_PATTERNS), regex=True, na=False)

    return df[entry_mask & tech_mask & ~exclude_mask]