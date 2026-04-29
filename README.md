# 🧪 Career Alchemist For All

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Pro%2FFlash-orange.svg)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**An open-source AI tool that rewrites your CV and cover letter to match any job description — for any professional, any industry.**

---

## 📌 What It Does

Job seekers spend countless hours manually tailoring their CVs to bypass Applicant Tracking Systems (ATS), often resulting in generic, low-impact bullet points.

**Career Alchemist For All** solves this. Upload your baseline CV and a target Job Description — the AI rewrites your professional experience using the **CAR framework** (Context, Action, Result), mirrors the exact keywords from the JD, and renders a beautifully formatted, executive-grade PDF.

No personal data is hardcoded. Works for any role, any industry, any professional.

---

## ⚙️ Quick Start

1. Clone the repo: `git clone https://github.com/jomigue79/Career-Alchemist-For-All.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with `GOOGLE_API_KEY=your_key_here`
4. Run the app: `streamlit run app.py`

> **Get a free API key**: [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Brain | Google Gemini 2.5 Pro (optimisation, cover letter) + Gemini 2.5 Flash (parsing, analysis) |
| UI Framework | Streamlit |
| PDF Rendering | WeasyPrint (HTML/CSS to PDF) |
| Template Engine | Jinja2 |
| Language | Python 3.10+ |

---

## 🚀 Key Features

- **CAR Framework Bullets** — Every rewritten bullet follows Context → Action → Result structure, starting with a strong action verb and closing with a quantifiable or qualitative impact.
- **Exact Keyword Mirroring** — Keywords and phrases from the JD are woven naturally into the rewritten CV to maximise ATS pass-through.
- **Anti-Hallucination Rules** — The optimizer never invents metrics, team sizes, or budget figures not present in your original CV.
- **CV–JD Match Evaluator** — Scores your CV against the JD across hard skills, soft skills, and qualifications, with a gap analysis.
- **Executive PDF Export** — Single-column navy-themed PDF with optional headshot, 3-column Core Competencies matrix, and inline role/period formatting.
- **Cover Letter Generator** — Structured 4-paragraph cover letter (Hook → Value Prop × 2 → CTA) as Markdown and downloadable PDF.
- **Smart Filenames** — Exported PDFs are named `name_role_company.pdf` automatically.

---

## 📁 Project Structure

```
app.py                   # Streamlit UI — main entry point
optimizer.py             # Rewrites CV bullets tailored to the JD (Gemini Pro)
cover_letter.py          # Generates structured cover letter (Gemini Pro)
match_evaluator.py       # Scores CV vs JD match with gap analysis (Gemini Flash)
requirement_extractor.py # Extracts structured requirements from the JD (Gemini Flash)
cv_parser.py             # Extracts static CV sections: skills, education, certs (Gemini Flash)
pdf_exporter.py          # Renders Jinja2 template to PDF via WeasyPrint
utils.py                 # Shared utilities: Gemini client, PDF text extraction, headshot processing
audit_test.py            # Smoke-test: structure, bullet syntax, and hallucination checks
packages.txt             # Linux system dependencies for Streamlit Cloud deployment
data/
  targets/               # Sample JD files for development
templates/
  cv_template.html       # Jinja2 CV template (WeasyPrint-safe layout)
  cv_style.css           # Executive navy theme
```

---

## 🔍 Audit

```bash
python audit_test.py
```

Expected output: `✅ AUDIT PASSED — 0 warnings across all content checks`
