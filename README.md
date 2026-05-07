# Job Market Analysis

This project analyzes entry-level technical job postings to identify high-frequency skills, common skill bundles, and broader patterns across technical role categories such as software, data science, and cybersecurity.

The pipeline loads raw job posting data, cleans and filters it to entry-level technical roles, extracts relevant skills, stores the structured results in PostgreSQL, runs descriptive SQL analysis, builds a job-skill matrix, applies clustering, and generates charts for interpretation.

## Project Goal

The goal of this project is to help students and entry-level candidates better understand which skills are most valuable in the technical job market.

Instead of relying on general advice, this project uses job posting data to answer questions such as:

- What are the most common skills in entry-level technical roles?
- What are the most common skills by role type?
- Which skills appear together most often?
- Can jobs be grouped into broader skill-based clusters?

## Features

- Loads historical tech job posting data from Kaggle
- Supports optional live job ingestion through JSearch
- Cleans and filters raw postings to entry-level technical roles
- Extracts skills from job titles and descriptions
- Stores structured results in PostgreSQL
- Exports SQL analysis results to CSV
- Builds a binary job-skill matrix
- Runs K-means clustering for multiple values of `k`
- Exports cluster summaries and charts

## Project Structure

```text
job-market-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── output/
│   ├── figures/
│   ├── logs/
│   └── tables/
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── src/
│   ├── main.py
│   ├── ingest/
│   ├── clean/
│   ├── skills/
│   ├── analysis/
│   ├── db/
│   ├── ml/
│   └── viz/
└── requirements.txt
```

## Requirements

- Python 3
- PostgreSQL
- A `.env` file for database credentials
- Optional: JSearch API key if live API fetching is enabled

## Environment Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## `.env` Setup

Create a `.env` file in the project root and add:

```env
DB_NAME=job_market_analysis
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

USE_JSEARCH=false
JSEARCH_API_KEY=your_jsearch_api_key_if_used
```

`USE_JSEARCH` is set to `false` by default to avoid unnecessary API usage and possible charges.

## PostgreSQL Setup

Create the database:

```bash
createdb -U postgres job_market_analysis
```

## How to Run

Run the full pipeline from the project root:

```bash
python3 src/main.py
```

This will:

- load and clean the dataset
- extract role types and skills
- save processed CSV files
- create and reset PostgreSQL tables
- insert cleaned data into the database
- export SQL analysis results
- build the job-skill matrix
- run clustering
- generate charts

## Main Outputs

### Processed data
Saved to `data/processed/`

- `cleaned_jobs.csv`
- `cleaned_jobs_with_skills.csv`
- `job_skill_matrix_baseline.csv`
- `job_skill_matrix_filtered.csv`
- `best_clustered_jobs.csv`

### SQL analysis outputs
Saved to `output/tables/`

- `role_type_counts.csv`
- `top_skills.csv`
- `avg_salary_by_role.csv`

### Clustering outputs
Saved to `output/tables/`

- `clustering_scores.csv`
- `best_cluster_counts.csv`
- `cluster_top_skills.csv`
- `cluster_role_types.csv`
- `cluster_top_titles.csv`

### Charts
Saved to `output/figures/`

- `role_type_counts.png`
- `top_skills.png`
- `avg_salary_by_role.png`
- `cluster_counts.png`
- `cluster_0_top_skills.png`
- `cluster_1_top_skills.png`
- `cluster_2_top_skills.png`
- `clustering_scores.png`

## Current Clustering Result

The best clustering result currently comes from `k = 3`.

These clusters broadly correspond to:

- Data Science / Machine Learning
- Software / Full-Stack Development
- Cybersecurity / Systems / Technical Infrastructure

## Notes

- The main runs currently use the Kaggle dataset by default.
- JSearch support is implemented but disabled by default for safety and cost control.
- The clustering stage uses a filtered job-skill matrix to reduce noise from overly common or overly rare skills.

## Future Improvements

- Improve skill extraction with more advanced NLP
- Compare additional clustering algorithms
- Add a user-facing interface for exploring skill gaps
- Re-enable live API enrichment in a controlled way
