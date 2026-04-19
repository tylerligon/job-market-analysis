import pandas as pd

def normalize_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]

    text_cols = [col for col in ["title", "company", "location", "job_description", "cleaned_description"] if col in df.columns]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

    for col in ["min_salary", "max_salary", "mean_salary"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df