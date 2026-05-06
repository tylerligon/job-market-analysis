import os
import logging
import re
from datetime import datetime
from dotenv import load_dotenv

from ingest.load_data import load_dataset
from ingest.fetch_api import fetch_jsearch_jobs
from ingest.merge import merge_sources
from clean.clean_jobs import clean_jobs
from skills.extract import add_skills_column
from analysis.frequency import top_skills
from analysis.role import add_role_type_column, role_type_counts, top_skills_by_role_type
from analysis.cooccurence import top_skill_pairs
from db.run_queries import run_analysis_queries
from db.reset_table import reset_tables
from db.create_tables import create_tables
from db.insert_jobs import insert_jobs

def setup_logging():
    load_dotenv()
    os.makedirs("output/logs", exist_ok=True)

    log_filename = datetime.now().strftime("output/logs/run_%Y-%m-%d_%H-%M-%S.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

    return log_filename


def main():
    log_file = setup_logging()
    logging.info("Starting pipeline")
    logging.info(f"Logging to: {log_file}")

    raw_path = "data/raw/all_jobs.xlsx"
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    kaggle_df = load_dataset(raw_path)
    logging.info(f"Kaggle original shape: {kaggle_df.shape}")

    try:
        api_df = fetch_jsearch_jobs(num_pages=1)
        logging.info(f"JSearch API original shape: {api_df.shape}")
    except Exception as e:
        logging.warning(f"JSearch fetch failed, continuing with Kaggle only: {e}")
        api_df = None
    
    merged_df = merge_sources(kaggle_df, api_df)
    logging.info(f"Merged sources original shape: {merged_df.shape}")

    cleaned_df = clean_jobs(merged_df)
    logging.info(f"Cleaned shape: {cleaned_df.shape}")

    cleaned_df.to_csv(f"{processed_dir}/cleaned_jobs.csv", index=False)
    logging.info("Saved cleaned_jobs.csv")

    cleaned_df = add_role_type_column(cleaned_df)
    cleaned_df = add_skills_column(cleaned_df)
    logging.info("Sample titles with skills:")


    #logging.info("\n" + cleaned_df[["title", "skills"]].head(10).to_string(index=False))
    #logging.info("Role type counts:")
    #logging.info(f"\n{role_type_counts(cleaned_df).to_string()}")
    #logging.info("Top skills by role type:")
    #for role_type, skills in top_skills_by_role_type(cleaned_df, top_n=10).items(): 
        #logging.info(f"{role_type}: {skills}")



    cleaned_df.to_csv(f"{processed_dir}/cleaned_jobs_with_skills.csv", index=False)
    logging.info("Saved cleaned_jobs_with_skills.csv")


    logging.info("Creating table databases if needed")
    create_tables()

    logging.info("Resetting tables if needed")
    reset_tables()

    logging.info("Inserting cleaned data into PostgreSQL")
    insert_jobs(cleaned_df)

    logging.info("Running analysis queries")
    run_analysis_queries()
    ##top_20 = top_skills(cleaned_df, 20)
    ##logging.info(f"Top 20 skills: {top_20}")

    ##top_20_pairs = top_skill_pairs(cleaned_df, 20)
    ##logging.info(f"Top 20 skill pairs: {top_20_pairs}")

    ##jobs_with_no_skills = (cleaned_df["skills"].str.len() == 0).sum()
    ##logging.info(f"Jobs with no detected skills: {jobs_with_no_skills}")

    logging.info("Pipeline finished successfully")


if __name__ == "__main__":
    main()