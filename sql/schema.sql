--need to create for db when we load data in
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    site TEXT,
    job_type TEXT,
    date_posted DATE,
    is_remote BOOLEAN,
    min_amount FLOAT,
    max_amount FLOAT,
    mean_salary FLOAT,
    interval TEXT,
    currency TEXT,
    role_type TEXT,
    description TEXT,
    cleaned_description TEXT
);

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name TEXT UNIQUE NOT NULL
);

CREATE TABLE job_skills (
    job_id TEXT REFERENCES jobs(job_id),
    skill_id INT REFERENCES skills(skill_id),
    PRIMARY KEY (job_id, skill_id)
);