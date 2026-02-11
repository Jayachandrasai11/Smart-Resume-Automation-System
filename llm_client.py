import os, json, requests, re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
PPLX_API_KEY = os.getenv("PPLX_API_KEY")

genai.configure(api_key=GENAI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-2.5-flash")

def extract_json_gemini(resume_text):
    prompt = f"""
    Extract structured information from this resume text.
    Return ONLY valid JSON with these fields:
    name, phone, email, education, skills, experience, projects

    Rules:
    - Never return null. Use "" for missing strings, [] for missing lists.
    - Always include all fields.
    - Return a single JSON object only.
    Resume:
    {resume_text}
    """
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

def safe_json_parse(raw_output):
    raw_output = raw_output.strip().replace("```json", "").replace("```", "")
    try:
        return json.loads(raw_output)
    except Exception:
        start, end = raw_output.find("{"), raw_output.rfind("}") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(raw_output[start:end])
            except Exception:
                return None
        return None

def fallback_extract(resume_text, data):
    # Email
    if not data.get("email"):
        match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
        if match:
            data["email"] = match.group(0)

    # Phone
    if not data.get("phone"):
        match = re.search(r"\+?\d[\d\s\-]{7,15}", resume_text)
        if match:
            data["phone"] = match.group(0)

    # Name
    if not data.get("name"):
        first_line = resume_text.split("\n")[0].strip()
        if len(first_line.split()) <= 4:
            data["name"] = first_line

    # Skills
    if not data.get("skills") or not data["skills"]:
        skill_keywords = [
            "Python", "FastAPI", "Django", "Flask", "PostgreSQL", "MySQL",
            "MongoDB", "SQL", "pgvector", "semantic search", "AWS", "Azure", "GCP",
            "Docker", "Kubernetes", "REST", "API", "GraphQL", "Java", "C++",
            "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"
        ]
        text_lower = resume_text.lower()
        found = [kw for kw in skill_keywords if kw.lower() in text_lower]
        data["skills"] = found

    return data
