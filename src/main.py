import os
import logging
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

from ingest.load_data import load_dataset
from ingest.fetch_api import fetch_jsearch_jobs
from ingest.merge import merge_sources
from clean.clean_jobs import clean_jobs
from skills.extract import add_skills_column
from skills.build_skill_matrix import build_skill_matrix
from analysis.role import add_role_type_column

from db.create_tables import create_tables
from db.reset_table import reset_tables
from db.insert_jobs import insert_jobs
from db.run_queries import run_analysis_queries

from ml.run_clustering import run_clustering_pipeline
from ml.cluster_summary import build_cluster_summary_tables


def setup_logging():
    load_dotenv()
    os.makedirs("output/logs", exist_ok=True)

    log_filename = datetime.now().strftime("output/logs/run_%Y-%m-%d_%H-%M-%S.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(),
        ],
    )

    return log_filename


def main():
    log_file = setup_logging()
    logging.info("Starting pipeline")
    logging.info(f"Logging to: {log_file}")

    # -------------------------
    # Paths / config
    # -------------------------
    raw_path = "data/raw/all_jobs.xlsx"
    processed_dir = "data/processed"
    output_tables_dir = "output/tables"
    api_cache_path = f"{processed_dir}/api_jobs_cleaned.csv"

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(output_tables_dir, exist_ok=True)

    use_jsearch = os.getenv("USE_JSEARCH", "false").lower() == "true"

    # -------------------------
    # Ingest
    # -------------------------
    kaggle_df = load_dataset(raw_path)
    logging.info(f"Kaggle original shape: {kaggle_df.shape}")

    if use_jsearch:
        try:
            api_df = fetch_jsearch_jobs(num_pages=1)
            logging.info(f"JSearch API original shape: {api_df.shape}")

            if not api_df.empty:
                api_df.to_csv(api_cache_path, index=False)
                logging.info("Saved JSearch API cache to CSV")
        except Exception as e:
            logging.warning(f"JSearch fetch failed, continuing with Kaggle only: {e}")
            api_df = pd.DataFrame()

    elif os.path.exists(api_cache_path):
        api_df = pd.read_csv(api_cache_path)
        logging.info("Loaded cached JSearch API data from CSV")

    else:
        logging.info("Skipping JSearch API fetch (USE_JSEARCH is false)")
        api_df = pd.DataFrame()

    if api_df.empty:
        merged_df = kaggle_df
        logging.info("Using Kaggle data only")
    else:
        merged_df = merge_sources(kaggle_df, api_df)
        logging.info("Merged Kaggle + JSearch data")

    logging.info(f"Merged sources original shape: {merged_df.shape}")

    # -------------------------
    # Clean / enrich
    # -------------------------
    cleaned_df = clean_jobs(merged_df)
    logging.info(f"Cleaned shape: {cleaned_df.shape}")

    cleaned_df = add_role_type_column(cleaned_df)
    cleaned_df = add_skills_column(cleaned_df)

    cleaned_df.to_csv(f"{processed_dir}/cleaned_jobs.csv", index=False)
    logging.info("Saved cleaned_jobs.csv")

    cleaned_df.to_csv(f"{processed_dir}/cleaned_jobs_with_skills.csv", index=False)
    logging.info("Saved cleaned_jobs_with_skills.csv")

    jobs_with_no_skills = (cleaned_df["skills"].str.len() == 0).sum()
    logging.info(f"Jobs with no detected skills: {jobs_with_no_skills}")

    ##logging.info("Sample titles with skills:")
    ##logging.info("\n" + cleaned_df[["title", "skills"]].head(10).to_string(index=False))

    # -------------------------
    # PostgreSQL
    # -------------------------
    logging.info("Creating tables if needed")
    create_tables()

    logging.info("Resetting tables")
    reset_tables()

    logging.info("Inserting cleaned data into PostgreSQL")
    insert_jobs(cleaned_df)

    logging.info("Running analysis queries")
    run_analysis_queries()

    # -------------------------
    # ML: skill matrix
    # -------------------------
    baseline_skill_matrix_df = build_skill_matrix(cleaned_df, min_skill_freq = 1, max_skill_ratio= 1.0)
    baseline_skill_matrix_df.to_csv(f"{processed_dir}/job_skill_matrix_baseline.csv", index=False)
    logging.info("Saved baseline job_skill_matrix.csv")

    skill_matrix_df = build_skill_matrix(cleaned_df, min_skill_freq=20, max_skill_ratio=0.4)
    skill_matrix_df.to_csv(f"{processed_dir}/job_skill_matrix_filtered.csv", index = False)
    logging.info("Saved filtered job_skill_matrix")


    # -------------------------
    # ML: clustering
    # -------------------------
    clustering_results = run_clustering_pipeline(
        skill_matrix_df,
        processed_dir=processed_dir,
        output_tables_dir=output_tables_dir,
        k_values=[3, 4, 5, 6],
    )

    logging.info(
        f"Best clustering result: k={clustering_results['best_k']} "
        f"with silhouette_score={clustering_results['best_score']:.4f}"
    )

    best_clustered_df = clustering_results["best_clustered_df"]

    if best_clustered_df is not None:
        cluster_skills_df, cluster_roles_df, cluster_titles_df = build_cluster_summary_tables(best_clustered_df)

        cluster_skills_df.to_csv(f"{output_tables_dir}/cluster_top_skills.csv", index=False)
        cluster_roles_df.to_csv(f"{output_tables_dir}/cluster_role_types.csv", index=False)
        cluster_titles_df.to_csv(f"{output_tables_dir}/cluster_top_titles.csv", index=False)

        logging.info("Saved cluster_top_skills.csv")
        logging.info("Saved cluster_role_types.csv")
        logging.info("Saved cluster_top_titles.csv")

    logging.info("Pipeline finished successfully")


if __name__ == "__main__":
    main()