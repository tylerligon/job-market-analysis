import pandas as pd

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