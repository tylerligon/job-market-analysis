##look for cooccurence

##basic 
from collections import Counter
from itertools import combinations

def top_skill_pairs(df, top_n=20):
    pair_counter = Counter()

    for skills in df["skills"]:
        unique_skills = sorted(set(skills))
        for pair in combinations(unique_skills, 2):
            pair_counter[pair] += 1

    return pair_counter.most_common(top_n)