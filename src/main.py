from ingest.load_data import load_dataset
from clean.clean_jobs import clean_jobs

def main():
    df = load_dataset("data/raw/all_jobs.xlsx")
    print("Original:", df.shape)

    df = clean_jobs(df)
    print("Cleaned:", df.shape)
    print(df.head())


    #checking random rows
    print(df["title"].head(20).tolist())
    print(df["title"].sample(20, random_state=42).tolist())
if __name__ == "__main__":
    main()