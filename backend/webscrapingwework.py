from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Setup headless Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

# Set path to your chromedriver
# Example: 'C:/Users/yourname/Downloads/chromedriver.exe' (Windows)
# or '/usr/local/bin/chromedriver' (Linux/Mac)

driver = webdriver.Chrome()

# Load the RemoteOK job page
url = "https://remoteok.com/remote-jobs"
driver.get(url)

# Wait for JavaScript to render jobs
time.sleep(5)

# Parse the page source
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Find the job table
table = soup.find("table", id="jobsboard")
job_elements = table.find_all("tr", class_=re.compile(".*job.*"))

print(f"Found {len(job_elements)} job postings.")

# Extract job data
jobs = []

for job in job_elements:
    job_title = job.find("h2", itemprop="title")
    company = job.find("h3", itemprop="name")
    location = job.find("div", class_="location")
    salary = location.find_next("div") if location else None
    tags = [tag.text.strip() for tag in job.find_all("div", class_="tag")]
    job_link = job.find("a", class_="preventLink")

    jobs.append({
        "title": job_title.text.strip() if job_title else "N/A",
        "company": company.text.strip() if company else "N/A",
        "location": location.text.strip() if location else "Remote",
        "salary": salary.text.strip() if salary else "N/A",
        "tags": ", ".join(tags),
        "link": "https://remoteok.com" + job_link["href"] if job_link else "N/A"
    })

# Save to Excel
df = pd.DataFrame(jobs)
df.to_excel("remote_jobs.xlsx", index=False, engine='openpyxl')
print("Saved job data to remote_jobs.xlsx")
