import pandas as pd

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()