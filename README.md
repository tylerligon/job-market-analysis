# job-market-analysis
CS210 Project: Analyzing skills, technologies, frameworks for undergraduate and entry-level candidates

# Title
Data-Driven Skill Matching for Early-Career Tech Jobs
# Overview
This project builds a pipeline that filters job postings and matches them to user skills to recommend the most relevant internships and entry-level tech roles.
# Features
1) Filters job postings for early-career tech roles
2) Extracts skills from job descriptions
3) Matches jobs to user skills
4) Ranks jobs based on how much skills are matched

# Pipeline:
Raw Data → Ingest → Clean/Filter → Extract Skills → Store in Database → Analyze → Cluster/Visualize

## Folder Structure

- `data/`: raw, merged, and cleaned job datasets
- `notebooks/`: experiments, charts, and quick analysis
- `sql/`: PostgreSQL schema and useful SQL queries
- `src/ingest/`: loads Kaggle data and API data
- `src/clean/`: filters early-career roles and standardizes columns
- `src/skills/`: extracts skills and builds skill features
- `src/db/`: creates tables and inserts data into PostgreSQL
- `src/analysis/`: skill frequency, role breakdowns, and bundles
- `src/ml/`: clustering and silhouette scoring
- `src/viz/`: final charts for presentation
- `outputs/`: saved graphs and final deliverables

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
