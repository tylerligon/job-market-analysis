import os
import logging
import pandas as pd

from ml.cluster_jobs import cluster_jobs


def run_clustering_pipeline(
    skill_matrix_df: pd.DataFrame,
    processed_dir: str = "data/processed",
    output_tables_dir: str = "output/tables",
    k_values: list[int] = None,
):
    if k_values is None:
        k_values = [3, 4, 5, 6]

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(output_tables_dir, exist_ok=True)

    clustering_scores = []

    best_score = -1
    best_k = None
    best_clustered_df = None

    for k in k_values:
        clustered_df, score = cluster_jobs(skill_matrix_df, k=k)
        clustering_scores.append({"k": k, "silhouette_score": score})
        logging.info(f"k={k} silhouette_score={score:.4f}")

        clustered_df.to_csv(f"{processed_dir}/clustered_jobs_k{k}.csv", index=False)

        if score > best_score:
            best_score = score
            best_k = k
            best_clustered_df = clustered_df

    scores_df = pd.DataFrame(clustering_scores)
    scores_df.to_csv(f"{output_tables_dir}/clustering_scores.csv", index=False)
    logging.info("Saved clustering_scores.csv")

    if best_clustered_df is not None:
        best_clustered_df.to_csv(f"{processed_dir}/best_clustered_jobs.csv", index=False)
        logging.info(f"Saved best_clustered_jobs.csv with k={best_k}")

        cluster_counts = (
            best_clustered_df["cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )
        cluster_counts.columns = ["cluster", "count"]
        cluster_counts.to_csv(f"{output_tables_dir}/best_cluster_counts.csv", index=False)
        logging.info("Saved best_cluster_counts.csv")

    return {
        "best_k": best_k,
        "best_score": best_score,
        "scores_df": scores_df,
        "best_clustered_df": best_clustered_df,
    }