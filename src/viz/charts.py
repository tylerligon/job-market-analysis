##create charts
import os
import pandas as pd
import matplotlib.pyplot as plt


def make_output_dirs():
    os.makedirs("output/figures", exist_ok=True)


def plot_role_type_counts(path="output/tables/role_type_counts.csv"):
    df = pd.read_csv(path)

    plt.figure(figsize=(8, 5))
    plt.bar(df["role_type"], df["count"])
    plt.title("Job Counts by Role Type")
    plt.xlabel("Role Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/figures/role_type_counts.png")
    plt.close()


def plot_top_skills(path="output/tables/top_skills.csv", top_n=10):
    df = pd.read_csv(path).head(top_n)

    plt.figure(figsize=(10, 6))
    plt.bar(df["skill_name"], df["count"])
    plt.title(f"Top {top_n} Skills Across All Jobs")
    plt.xlabel("Skill")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("output/figures/top_skills.png")
    plt.close()


def plot_avg_salary_by_role(path="output/tables/avg_salary_by_role.csv"):
    df = pd.read_csv(path)

    plt.figure(figsize=(8, 5))
    plt.bar(df["role_type"], df["avg_salary"])
    plt.title("Average Salary by Role Type")
    plt.xlabel("Role Type")
    plt.ylabel("Average Salary")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/figures/avg_salary_by_role.png")
    plt.close()


def plot_cluster_counts(path="output/tables/best_cluster_counts.csv"):
    df = pd.read_csv(path)


    plt.figure(figsize=(6, 4))
    plt.bar(df["cluster"].astype(int), df["count"].astype(int))
    plt.title("Job Counts by Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/figures/cluster_counts.png")
    plt.close()


def plot_top_skills_per_cluster(path="output/tables/cluster_top_skills.csv", top_n=10):
    df = pd.read_csv(path)

    for cluster_id in sorted(df["cluster"].unique()):
        cluster_df = df[df["cluster"] == cluster_id].head(top_n).copy()
        cluster_df["count"] = pd.to_numeric(cluster_df["count"])


        plt.figure(figsize=(10, 6))
        plt.bar(cluster_df["skill"], cluster_df["count"])
        plt.title(f"Top {top_n} Skills in Cluster {cluster_id}")
        plt.xlabel("Skill")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(f"output/figures/cluster_{cluster_id}_top_skills.png")
        plt.close()


def plot_clustering_scores(path="output/tables/clustering_scores.csv"):
    df = pd.read_csv(path)

    plt.figure(figsize=(6, 4))
    plt.plot(df["k"], df["silhouette_score"], marker="o")
    plt.title("Silhouette Score by k")
    plt.xlabel("k")
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    plt.savefig("output/figures/clustering_scores.png")
    plt.close()


def make_all_charts():
    make_output_dirs()
    plot_role_type_counts()
    plot_top_skills()
    plot_avg_salary_by_role()
    plot_cluster_counts()
    plot_top_skills_per_cluster()
    plot_clustering_scores()
    print("All charts saved to output/figures/")