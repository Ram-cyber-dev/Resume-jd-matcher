import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------- UI SETUP ----------------
st.set_page_config(page_title="Resume ↔ JD Matcher", page_icon="🧩", layout="centered")
st.title("🧩 Resume ↔ Job Description Matcher")
st.caption("Paste your resume and a job description → get match %, missing skills, and improvement tips.")

# ---------------- LOAD API KEY ----------------
load_dotenv()

api_key = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Add it to .env (local) or Streamlit secrets (cloud).")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

# ---------------- INPUTS ----------------
resume = st.text_area("📄 Paste Resume", height=220, placeholder="Paste resume text here...")
jd = st.text_area("🧾 Paste Job Description", height=220, placeholder="Paste job description here...")

role = st.text_input("🎯 Target Role (optional)", placeholder="e.g., Data Analyst, Backend Developer")

strictness = st.select_slider(
    "Matching strictness",
    options=["Lenient", "Balanced", "Strict"],
    value="Balanced"
)

go = st.button("Match Now", type="primary")

# ---------------- PROMPT + AI CALL ----------------
def build_prompt(resume_text: str, jd_text: str, role_text: str, strict: str) -> str:
    return f"""
You are an ATS + hiring manager.

Task:
Compare the RESUME to the JOB DESCRIPTION and output ONLY valid JSON.

Strictness: {strict}
Target role (optional): {role_text if role_text.strip() else "Not provided"}

Rules:
- Be realistic (no inflated scores).
- Consider hard skills, tools, keywords, years/level, and relevant projects.
- If resume is missing something important, mark it missing.

Output JSON schema (must match exactly):
{{
  "match_percentage": 0,
  "match_level": "Low/Medium/High",
  "top_matching_skills": ["..."],
  "missing_or_weak_skills": ["..."],
  "keyword_gaps": ["..."],
  "resume_improvements": ["..."],
  "summary": "..."
}}

RESUME:
{resume_text}

JOB_DESCRIPTION:
{jd_text}
"""

def safe_json_parse(text: str):
    # Try direct JSON parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try extracting JSON block if model wraps it
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except Exception:
            return None
    return None

if go:
    if not resume.strip() or not jd.strip():
        st.warning("Please paste BOTH the resume and job description.")
        st.stop()

    with st.spinner("Matching..."):
        prompt = build_prompt(resume, jd, role, strictness)

        try:
            resp = client.models.generate_content(model=MODEL, contents=prompt)
            raw = resp.text or ""
            data = safe_json_parse(raw)

            if not data:
                st.error("AI returned non-JSON output. Showing raw output below.")
                st.code(raw)
                st.stop()

            # ---------------- DISPLAY ----------------
            st.subheader("✅ Match Result")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Match %", f"{data.get('match_percentage', 0)}%")
            with col2:
                st.metric("Match Level", data.get("match_level", "Unknown"))

            st.write("**Summary**")
            st.write(data.get("summary", ""))

            st.write("**Top Matching Skills**")
            st.write(data.get("top_matching_skills", []))

            st.write("**Missing / Weak Skills**")
            st.write(data.get("missing_or_weak_skills", []))

            st.write("**Keyword Gaps**")
            st.write(data.get("keyword_gaps", []))

            st.write("**Resume Improvements**")
            st.write(data.get("resume_improvements", []))

            with st.expander("🔍 Raw JSON"):
                st.json(data)

        except Exception as e:
            st.error(f"Gemini API error: {e}")
