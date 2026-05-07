import pandas as pd
'''
def build_skill_matrix(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "skills" not in df.columns:
        raise ValueError("DataFrame must contain a 'skills' column.")

    exploded = df["skills"].explode()

    # clean exploded skill values
    exploded = exploded.dropna()
    exploded = exploded.astype(str).str.strip().str.lower()
    exploded = exploded[exploded != ""]

    # rows = original job index, columns = skill names
    skill_dummies = pd.crosstab(exploded.index, exploded)

    # keep metadata from original dataframe
    meta_cols = [col for col in ["id", "title", "company", "role_type"] if col in df.columns]
    meta = df[meta_cols]

    # align on original dataframe index
    result = meta.join(skill_dummies, how="left").fillna(0)

    # make skill columns ints instead of floats
    skill_cols = [col for col in result.columns if col not in meta_cols]
    result[skill_cols] = result[skill_cols].astype(int)

    return result.reset_index(drop=True)
'''

def build_skill_matrix(
    df: pd.DataFrame,
    min_skill_freq: int = 20,
    max_skill_ratio: float = 0.40,
) -> pd.DataFrame:
    df = df.copy()

    if "skills" not in df.columns:
        raise ValueError("DataFrame must contain a 'skills' column.")

    exploded = df["skills"].explode()

    exploded = exploded.dropna()
    exploded = exploded.astype(str).str.strip().str.lower()
    exploded = exploded[exploded != ""]

    skill_dummies = pd.crosstab(exploded.index, exploded)

    # filter overly rare / overly common skills
    n_jobs = len(df)
    skill_counts = skill_dummies.sum(axis=0)

    keep_cols = skill_counts[
        (skill_counts >= min_skill_freq) &
        (skill_counts <= n_jobs * max_skill_ratio)
    ].index

    skill_dummies = skill_dummies[keep_cols]

    meta_cols = [col for col in ["id", "title", "company", "role_type"] if col in df.columns]
    meta = df[meta_cols]

    result = meta.join(skill_dummies, how="left").fillna(0)

    skill_cols = [col for col in result.columns if col not in meta_cols]
    result[skill_cols] = result[skill_cols].astype(int)

    return result.reset_index(drop=True)