# Resume-JD Matcher

A Streamlit app that analyzes how well your resume matches a job description using Google's Gemini 2.5 Flash. Enter your resume and a job description — get a match percentage, missing skills, keyword gaps, and improvement suggestions.

## Features

- **ATS-style matching** — compares your resume against any job description
- **Match score** — percentage + Low/Medium/High level
- **Skill gap analysis** — lists missing or weak skills
- **Keyword gap detection** — highlights important keywords your resume is missing
- **Improvement suggestions** — actionable tips to strengthen your resume
- **Adjustable strictness** — Lenient, Balanced, or Strict mode

## Quick Start

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Run:
```bash
streamlit run app.py
```

## Tech Stack

- **Streamlit** — UI framework
- **Google Gemini 2.5 Flash** — AI matching engine
- **Python** — application logic

## Demo

Paste your resume text, paste a job description, adjust strictness, click Match Now. The AI returns a structured JSON response with match percentage, skill gaps, keyword gaps, and improvement tips — all displayed in a clean dashboard.
