#common technical skills to detect
SKILL_KEYWORDS = [
    "python", "sql", "java", "javascript", "typescript", "c++", "c#",
    "react", "node", "aws", "azure", "gcp", "excel", "tableau", "power bi",
    "pandas", "numpy", "tensorflow", "pytorch", "docker", "kubernetes",
    "git", "linux", "machine learning", "data analysis", "spark"
]

# extract skills from job description text
def extract_skills(text):
    text = str(text).lower()
    found = []

# loops through the list of skills to match with skills listed on job description  
    for skill in SKILL_KEYWORDS:
        if skill in text:
            found.append(skill)
          
# remove the dupes and sort them
    return sorted(set(found))

# compare the job skills with the users skills
def score_match(job_skills, user_skills):

# both lists are converted to sets for comparison
    job_set = set(s.lower() for s in job_skills)
    user_set = set(s.lower() for s in user_skills)

# return 0 if job has no skills
    if not job_set:
        return 0
# number of matching skills matches with the returned score
    return len(job_set.intersection(user_set))
