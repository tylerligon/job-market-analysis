import pandas as pd
from clean.normalize_fields import normalize_fields
from clean.deduplicate import deduplicate
from clean.handle_missing import handle_missing
from clean.filter_roles import filter_roles

def clean_jobs(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_fields(df)
    df = deduplicate(df)
    df = handle_missing(df)
    df = filter_roles(df)
    return df