CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    site TEXT,
    job_type TEXT,
    date_posted DATE,
    is_remote BOOLEAN,
    min_amount DOUBLE PRECISION,
    max_amount DOUBLE PRECISION,
    mean_salary DOUBLE PRECISION,
    interval TEXT,
    currency TEXT,
    role_type TEXT,
    description TEXT,
    cleaned_description TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id TEXT REFERENCES jobs(job_id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(skill_id) ON DELETE CASCADE,
    PRIMARY KEY (job_id, skill_id)
);