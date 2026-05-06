-- Total jobs
SELECT COUNT(*) FROM jobs;

-- Jobs by role type
SELECT role_type, COUNT(*) AS count
FROM jobs
GROUP BY role_type
ORDER BY count DESC;

-- Top 20 skills
SELECT s.skill_name, COUNT(*) AS count
FROM job_skills js
JOIN skills s ON js.skill_id = s.skill_id
GROUP BY s.skill_name
ORDER BY count DESC
LIMIT 20;

-- Top companies by number of jobs
SELECT company, COUNT(*) AS count
FROM jobs
GROUP BY company
ORDER BY count DESC
LIMIT 20;

-- Remote vs non-remote
SELECT is_remote, COUNT(*) AS count
FROM jobs
GROUP BY is_remote
ORDER BY count DESC;

-- Average salary by role type
SELECT role_type, AVG(mean_salary) AS avg_salary
FROM jobs
WHERE mean_salary IS NOT NULL
GROUP BY role_type
ORDER BY avg_salary DESC;

-- Top 10 companies by average salary
SELECT company, AVG(mean_salary) AS avg_salary, COUNT(*) AS job_count
FROM jobs
WHERE mean_salary IS NOT NULL
GROUP BY company
HAVING COUNT(*) >= 3
ORDER BY avg_salary DESC
LIMIT 10;

-- Average salary by role type
SELECT role_type, ROUND(AVG(mean_salary)::numeric, 2) AS avg_salary
FROM jobs
WHERE mean_salary IS NOT NULL
GROUP BY role_type
ORDER BY avg_salary DESC;

-- Top remote-friendly role types
SELECT role_type, COUNT(*) AS remote_count
FROM jobs
WHERE is_remote = TRUE
GROUP BY role_type
ORDER BY remote_count DESC;

-- Top skills for software roles
SELECT s.skill_name, COUNT(*) AS count
FROM job_skills js
JOIN skills s ON js.skill_id = s.skill_id
JOIN jobs j ON js.job_id = j.job_id
WHERE j.role_type = 'software'
GROUP BY s.skill_name
ORDER BY count DESC
LIMIT 10;

-- Top skills for data roles
SELECT s.skill_name, COUNT(*) AS count
FROM job_skills js
JOIN skills s ON js.skill_id = s.skill_id
JOIN jobs j ON js.job_id = j.job_id
WHERE j.role_type = 'data'
GROUP BY s.skill_name
ORDER BY count DESC
LIMIT 10;

-- Top skills for cybersecurity roles
SELECT s.skill_name, COUNT(*) AS count
FROM job_skills js
JOIN skills s ON js.skill_id = s.skill_id
JOIN jobs j ON js.job_id = j.job_id
WHERE j.role_type = 'cybersecurity'
GROUP BY s.skill_name
ORDER BY count DESC
LIMIT 10;