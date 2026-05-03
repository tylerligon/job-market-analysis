#RUN EVERYTHING THROUGH HERE
#main pipeline runner, loads data, cleans it, extract skills, and saves output
from ingest.load_data import load_dataset
from clean.clean_jobs import clean_jobs
from skills.extract import add_skills_column
from analysis.frequency import top_skills
import pandas as pd

def main():
    df = load_dataset("data/raw/all_jobs.xlsx")
    print("Original:", df.shape)

    df = clean_jobs(df)
    print("Cleaned:", df.shape)
    print(df.head())

    df = add_skills_column(df)
    print(df[["title", "skills"]].head(10))
    print(top_skills(df, 10))

    df.to_csv("data/processed/cleaned_jobs.csv", index = False)

if __name__ == "__main__":
    main()