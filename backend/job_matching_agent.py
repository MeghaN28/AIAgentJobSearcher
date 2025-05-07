import pandas as pd
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load parsed resume data (JSON)
def load_parsed_resume(file_path="parsed_resume.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        resume_data = json.load(f)
    return resume_data

# Load job listings from Excel
def load_job_listings(file_path="remote_jobs.xlsx"):
    return pd.read_excel(file_path)

# Score job listings based on skills, experience, and interests
def score_job_match(resume_data, job_data):
    # Skills match (fuzzy matching on resume skills vs job tags)
    skill_match_score = 0
    job_tags = job_data.get('tags', "")
    skills = resume_data.get("skills", [])
    
    if skills:  # Ensure skills list is not empty
        # Match skills to job tags
        for skill in skills:
            for tag in job_tags.split(","):
                skill_match_score += fuzz.partial_ratio(skill.lower(), tag.lower()) / 100
        
        # Normalize skill match score (max score will be the number of skills)
        skill_match_score = min(skill_match_score / len(skills), 1)
    else:
        skill_match_score = 0  # If no skills are provided, score is 0

    # Role relevance score (matches between experience and job title)
    role_relevance_score = fuzz.partial_ratio(resume_data.get("experience", {}).get("recentRoles", [{}])[0].get("title", "").lower(), job_data.get("title", "").lower()) / 100

    # Interest alignment score (match interests with job tags or description)
    interest_match_score = 0
    interests = resume_data.get("interests", [])
    if interests:  # Ensure interests list is not empty
        for interest in interests:
            for tag in job_tags.split(","):
                interest_match_score += fuzz.partial_ratio(interest.lower(), tag.lower()) / 100
        
        # Normalize interest match score
        interest_match_score = min(interest_match_score / len(interests), 1)
    else:
        interest_match_score = 0  # If no interests are provided, score is 0

    # Calculate total match score (weights: 50% skills, 30% role relevance, 20% interests)
    total_score = (skill_match_score * 0.5) + (role_relevance_score * 0.3) + (interest_match_score * 0.2)

    return total_score

# Main function to match jobs with parsed resume
def match_jobs(parsed_resume_path="parsed_resume.json", job_listings_path="remote_jobs.xlsx"):
    # Load the parsed resume and job listings
    resume_data = load_parsed_resume(parsed_resume_path)
    job_listings_df = load_job_listings(job_listings_path)

    # List to store job scores and details
    matched_jobs = []

    # Loop through job listings and calculate match scores
    for _, job in job_listings_df.iterrows():
        job_data = {
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "salary": job["salary"],
            "tags": job["tags"],
            "link": job["link"]
        }
        
        score = score_job_match(resume_data, job_data)
        job_data["match_score"] = score
        
        matched_jobs.append(job_data)

    # Sort jobs by match score in descending order
    matched_jobs = sorted(matched_jobs, key=lambda x: x["match_score"], reverse=True)
    
    return matched_jobs

# Function to save the matched jobs to an Excel file
def save_matched_jobs(matched_jobs, output_path="matched_jobs.xlsx"):
    matched_jobs_df = pd.DataFrame(matched_jobs)
    matched_jobs_df.to_excel(output_path, index=False)
    print(f"✅ Matched jobs saved to {output_path}")

# Example usage
if __name__ == "__main__":
    matched_jobs = match_jobs()
    # Optionally save the results
    save_matched_jobs(matched_jobs)
    # Print out the top 5 matches
    for job in matched_jobs[:5]:
        print(f"Job Title: {job['title']}, Company: {job['company']}, Match Score: {job['match_score']:.2f}")
