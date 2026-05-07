import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def cluster_jobs(skill_matrix_df: pd.DataFrame, k: int = 4):
    feature_cols = [
        col for col in skill_matrix_df.columns
        if col not in ["id", "title", "company", "role_type"]
    ]

    X = skill_matrix_df[feature_cols]

    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X)

    clustered_df = skill_matrix_df.copy()
    clustered_df["cluster"] = labels

    score = silhouette_score(X, labels)

    return clustered_df, score

