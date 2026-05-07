from collections import Counter
import pandas as pd


def top_skills_by_cluster(clustered_df: pd.DataFrame, top_n: int = 10) -> dict[int, list[tuple[str, int]]]:
    meta_cols = {"id", "title", "company", "role_type", "cluster"}
    skill_cols = [col for col in clustered_df.columns if col not in meta_cols]

    results = {}
    for cluster_id, group in clustered_df.groupby("cluster"):
        skill_totals = group[skill_cols].sum().sort_values(ascending=False)
        results[int(cluster_id)] = list(skill_totals.head(top_n).items())

    return results


def role_type_by_cluster(clustered_df: pd.DataFrame) -> dict[int, list[tuple[str, int]]]:
    results = {}
    for cluster_id, group in clustered_df.groupby("cluster"):
        counts = group["role_type"].value_counts()
        results[int(cluster_id)] = list(counts.items())
    return results


def top_titles_by_cluster(clustered_df: pd.DataFrame, top_n: int = 10) -> dict[int, list[tuple[str, int]]]:
    results = {}
    for cluster_id, group in clustered_df.groupby("cluster"):
        counts = group["title"].value_counts().head(top_n)
        results[int(cluster_id)] = list(counts.items())
    return results


def build_cluster_summary_tables(clustered_df: pd.DataFrame):
    skill_rows = []
    for cluster_id, items in top_skills_by_cluster(clustered_df, top_n=10).items():
        for skill, count in items:
            skill_rows.append({
                "cluster": cluster_id,
                "skill": skill,
                "count": int(count),
            })

    role_rows = []
    for cluster_id, items in role_type_by_cluster(clustered_df).items():
        for role_type, count in items:
            role_rows.append({
                "cluster": cluster_id,
                "role_type": role_type,
                "count": int(count),
            })

    title_rows = []
    for cluster_id, items in top_titles_by_cluster(clustered_df, top_n=10).items():
        for title, count in items:
            title_rows.append({
                "cluster": cluster_id,
                "title": title,
                "count": int(count),
            })

    return (
        pd.DataFrame(skill_rows),
        pd.DataFrame(role_rows),
        pd.DataFrame(title_rows),
    )