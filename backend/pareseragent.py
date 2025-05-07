import os
import fitz  # PyMuPDF
import google.generativeai as genai
import json

# ---------- 1. Configure Gemini ----------
genai.configure(api_key="abc")  # Replace with your actual key

model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- 2. Resume Text Extractor ----------
def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    return "\n".join([page.get_text() for page in doc])

# ---------- 3. General Resume Parser ----------
def parse_resume_with_gemini(resume_text: str) -> dict:
    prompt = f"""
You are a smart resume parser agent. Read the resume below and extract the following into a JSON:

1. "skills": List of all technical and soft skills
2. "experience": Summary of work experience (total years, recent roles)
3. "interests": Inferred from projects, volunteering, or explicitly stated
4. Ensure it's valid JSON with keys: skills, experience, interests.

Resume:
\"\"\"{resume_text}\"\"\"
"""
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e), "raw_response": response.text}


# ---------- 4. Agent Runner ----------
def parse_resume(file_path: str):
    resume_text = extract_text_from_pdf(file_path)
    result = parse_resume_with_gemini(resume_text)
    return result


# ---------- 5. Run with a sample file ----------
if __name__ == "__main__":
    file_path = "Megha_N_resume_2025.pdf"  # Replace with your resume file path
    output = parse_resume(file_path)
    parsed_data_path = "parsed_resume.json"
with open(parsed_data_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)
