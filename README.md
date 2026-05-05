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

### 1. Create and activate the virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
Add:

```env
JSEARCH_API_KEY=your_jsearch_api_key
DB_NAME=job_market_analysis
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Create the PostgreSQL database
```bash
createdb -U postgres job_market_analysis
```

### 5. Create the database tables
```bash
python3 -m src.db.create_tables
```

### 6. Run the full pipeline
```bash
python3 src/main.py
```

### 7. Insert cleaned data into PostgreSQL
```bash
python3 -m src.db.insert_jobs
```