##merge data together
import pandas as pd

def merge_sources(kaggle_df: pd.DataFrame, api_df: pd.DataFrame) -> pd.DataFrame:
    merged = pd.concat([kaggle_df, api_df], ignore_index=True, sort=False)
    return merged