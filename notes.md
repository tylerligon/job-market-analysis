What each folder does:
data/: raw, merged, and cleaned files
notebooks/: quick experimentation and charts
sql/: PostgreSQL schema and useful queries
src/ingest/: pulls in Kaggle/API data
src/clean/: filters to internship/new grad/entry-level and standardizes fields
src/skills/: extracts skills and builds the feature matrix
src/db/: inserts cleaned data into Postgres
src/analysis/: top skills, top bundles, role breakdowns
src/ml/: clustering and silhouette scoring
src/viz/: final charts/results for presentation
outputs/: saved graphs and final deliverables


Probably build first:
src/ingest/load_dataset.py
src/ingest/fetch_api.py
src/clean/filter_roles.py
src/clean/normalize_fields.py
src/skills/extract_skills.py
src/db/create_tables.py
src/db/insert_jobs.py
src/analysis/frequency_analysis.py

Good order:
ingest data
clean and filter
extract skills
store in Postgres
run analysis
do clustering last


Everything will run through main.py, we just build each file and call the functions from main.py.
To set up a .venv environment:
python3 -m venv .venv
source .venv/bin/activate

Want to put all imports and libraries into requirements.txt for last