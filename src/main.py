import os
import logging
from datetime import datetime

from ingest.load_data import load_dataset
from clean.clean_jobs import clean_jobs
from skills.extract import add_skills_column
from analysis.frequency import top_skills


def setup_logging():
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

    df = load_dataset(raw_path)
    logging.info(f"Original shape: {df.shape}")

    df = clean_jobs(df)
    logging.info(f"Cleaned shape: {df.shape}")

    df.to_csv(f"{processed_dir}/cleaned_jobs.csv", index=False)
    logging.info("Saved cleaned_jobs.csv")

    df = add_skills_column(df)

    logging.info("Sample titles with skills:")
    logging.info("\n" + df[["title", "skills"]].head(10).to_string(index=False))

    df.to_csv(f"{processed_dir}/cleaned_jobs_with_skills.csv", index=False)
    logging.info("Saved cleaned_jobs_with_skills.csv")

    top_20 = top_skills(df, 20)
    logging.info(f"Top 20 skills: {top_20}")

    jobs_with_no_skills = (df["skills"].str.len() == 0).sum()
    logging.info(f"Jobs with no detected skills: {jobs_with_no_skills}")

    logging.info("Pipeline finished successfully")


if __name__ == "__main__":
    main()