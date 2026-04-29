# 🧪 The Career Alchemist

**AI-Driven Executive Career Optimisation — governed by PM²**

## 📌 Project Overview

The Career Alchemist is a professional-grade Career Intelligence tool designed for Technical Project Managers and senior professionals. Unlike generic CV builders, this system uses an AI pipeline to align a candidate's professional history with a specific Job Description (JD) while strictly preserving their authentic voice and refusing to hallucinate facts.

The core engine uses **Google Gemini 2.5 Pro/Flash** and a custom **Voice Profile** (`data/voice_params.json`) to transform a baseline CV into a high-impact, ATS-optimised application — complete with tailored PDF export and a structured cover letter.

## ⚙️ Installation & Setup

1. Clone the repo: `git clone https://github.com/jomigue79/career-alchemist.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with `GOOGLE_API_KEY=your_key_here`
4. Run the app: `streamlit run app.py`

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Brain | Google Gemini 2.5 Pro (optimisation, cover letter) + Gemini 2.5 Flash (parsing, analysis) |
| UI Framework | Streamlit |
| PDF Rendering | WeasyPrint (HTML/CSS → PDF — `display: flex` not supported; uses `display: table`) |
| Template Engine | Jinja2 |
| Language | Python 3.10+ |
| Governance | PM² Methodology |

## 🚀 Key Features

- **Action-Governance-Impact Bullets** — Every rewritten bullet starts with a strong action verb, includes methodological context, and closes with a qualitative or quantitative impact statement.
- **Voice Profile Injection** — A `voice_params.json` persona profile is injected into every prompt to maintain an analytical, authoritative "Systems Architect" tone across all outputs.
- **Anti-Hallucination Rules** — The optimizer is strictly instructed never to invent metrics, team sizes, or budget figures not present in the baseline CV, and never to sum experience years across roles.
- **CV–JD Match Evaluator** — Scores the CV against the JD across hard skills, soft skills, and qualifications, with a gap analysis and recommendation.
- **Executive PDF Export** — Generates a single-column navy-themed PDF with a circular headshot, 3-column Core Competencies matrix, and inline role/period formatting.
- **Cover Letter Generator** — Produces a structured 4-paragraph cover letter (Hook → Evidence × 2 → Close) as both Markdown and a downloadable PDF.
- **Smart Filenames** — Exported PDFs are named `name_role_company.pdf` automatically.

## 🏛️ Project Governance (PM²)

This project was developed following the PM² lifecycle:

- **Initiating** — Defined scope: tailored CV + cover letter generation for a specific candidate persona.
- **Planning** — Designed the AI agent pipeline, voice profile schema, and PDF template architecture.
- **Executing** — Built the Analyst, Evaluator, Optimizer, and Writer agents; iterated on prompt engineering and WeasyPrint layout constraints.
- **Closing** — Full code audit, dead-file removal, module documentation, and pipeline validation via `audit_test.py`.

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
audit_test.py            # Smoke-test: validates AI output structure, bullet syntax, hallucination checks
data/
  voice_params.json      # Candidate voice profile injected into all prompts
  voice_profile.md       # Human-readable reference for the voice profile
  targets/               # Sample JD files for development and batch analysis
templates/
  cv_template.html       # Jinja2 CV template (WeasyPrint-safe layout)
  cv_style.css           # Executive navy theme
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- GTK+ 3 runtime (Windows only — required by WeasyPrint): [GTK installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
- A Google AI API key with access to Gemini 2.5 models

### Installation

```bash
git clone https://github.com/jomigue79/career-alchemist.git
cd career-alchemist
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=AIza...
```

### Run

```bash
streamlit run app.py
```

### Audit

```bash
python audit_test.py
```

Expected output: `✅ AUDIT PASSED — 0 warnings across all content checks`
