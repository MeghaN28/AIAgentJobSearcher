from langchain.tools import tool
from preprocess import job_data
@tool
def recommend_jobs(resume: str) -> str:
    """
    Recommend the top 5 relevant jobs based on a user's resume or profile.
    """
    from difflib import SequenceMatcher

    # Basic string matching for now
    def match_score(resume_text, job_text):
        return SequenceMatcher(None, resume_text.lower(), job_text.lower()).ratio()

    job_scores = []
    for job in job_data:
        combined = f"{job['title']} {job['company']} {job['location']} {job['tags']}"
        score = match_score(resume, combined)
        job_scores.append((score, job))

    top_jobs = sorted(job_scores, key=lambda x: x[0], reverse=True)[:5]

    return "\n\n".join([
        f"🔹 **{job['title']}** at **{job['company']}**\n📍 Location: {job['location']}\n💰 Salary: {job['salary']}\n🏷️ Tags: {job['tags']}\n🔗 [Apply here]({job['link']})"
        for _, job in top_jobs
    ])
