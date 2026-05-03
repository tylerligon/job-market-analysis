#look at frequencies, this is just a test
from collections import Counter

def top_skills(df, top_n=20):
    counter = Counter()

    for skills in df["skills"]:
        counter.update(skills)

    return counter.most_common(top_n)