import pandas as pd

def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required = [col for col in ["title", "cleaned_description"] if col in df.columns]
    if required:
        df = df.dropna(subset=required)

    return df