import pandas as pd

# Load and clean job data
df = pd.read_excel("remote_jobs.xlsx")
df.dropna(subset=["title", "company", "location", "link"], inplace=True)
df["tags"] = df["tags"].fillna("")

# Create job records as a list of dicts
job_data = df.apply(lambda row: {
    "title": row["title"],
    "company": row["company"],
    "location": row["location"],
    "salary": row["salary"],
    "tags": row["tags"],
    "link": row["link"]
}, axis=1).tolist()
