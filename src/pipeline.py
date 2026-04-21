import pandas as pd
from filters import filter_jobs
from skills import extract_skills, score_match

# main pipeline function
def run_pipeline(csv_path, user_skills):
    # load dataset
    df = pd.read_csv(csv_path)

    # filter jobs 
    filtered = filter_jobs(df)

    # extract skills from each job description
    filtered["extracted_skills"] = filtered["description"].apply(extract_skills)

    # score how well each job matches the user's skills
    filtered["match_score"] = filtered["extracted_skills"].apply(
        lambda skills: score_match(skills, user_skills)
    )

    # sort jobs by best match first
    filtered = filtered.sort_values(
        by=["match_score", "title"],
        ascending=[False, True]
    )

    return filtered

# runs when executing file directly
if __name__ == "__main__":
    # example user skills
    user_skills = ["python", "sql", "excel", "aws"]

    # run the pipeline
    results = run_pipeline("data/sample_jobs.csv", user_skills)

    # print top results
    print(results[["title", "company", "location", "extracted_skills", "match_score"]].head(20))
