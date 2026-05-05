"""
optimizer.py
Rewrites the CV's Professional Summary and Experience section using Gemini Pro,
tailored to a specific Job Description.

System role: Universal ATS Optimizer & Executive Career Strategist

Process (internal to the prompt):
  STEP 1 — JD Keyword Extraction: identify top 6-8 mandatory hard/soft/methodological keywords
  STEP 2 — CV Rewrite: CAR-framework bullets, keyword mirroring, no invented facts

Strict anti-hallucination rules enforced:
  - No invented metrics, team sizes, or budgets
  - No summing of years across different roles
  - No skills or experience not present in the baseline CV

Returns a dict: { "summary": str, "experience": [{ company, role, period, bullets }] }
"""
import json
from utils import groq_client, GROQ_MODEL


def get_tailored_cv(cv_text, jd_text):
    """
    Rewrites CV bullets and summary tailored to a JD using the CAR framework.
    Returns a parsed dict with 'summary' and 'experience' keys.
    """
    system_prompt = """You are an elite Executive Career Strategist and ATS Optimization Engine.
Rewrite the CV's Professional Summary and Experience to achieve a 90%+ ATS match with the Job Description.

VOICE PHILOSOPHY: Executive Achiever tone — impact-driven, objective, no buzzwords. Implied first-person (NEVER use I/my/we in bullets).
SYNTAX: Every bullet MUST start with a strong past-tense action verb. Use CAR framework (Context, Action, Result).
KEYWORDS: Extract top 6-8 mandatory JD keywords. Mirror exact JD terminology in rewrites.
ANTI-HALLUCINATION:
- Never invent metrics, figures, or facts not in the CV.
- Never invent skills not present in the CV.
- Never sum years across different roles.

Return ONLY valid JSON (no markdown, no explanation) with this exact structure:
{
  "summary": "3-sentence executive summary tailored to this JD",
  "experience": [
    {
      "company": "Company Name",
      "role": "Role Name",
      "period": "Jan 2020 – Dec 2022",
      "bullets": ["bullet 1", "bullet 2", "bullet 3"]
    }
  ]
}
IMPORTANT: Begin your response immediately with `{`. Do not echo, repeat, or output any input text before the JSON."""
    user_content = (
        "===BASELINE CV (ground truth — do not invent beyond this)===\n" + cv_text
        + "\n\n===TARGET JOB DESCRIPTION===\n" + jd_text
    )

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
    except Exception as e:
        raise RuntimeError(f"Groq API error during CV optimization: {e}") from e

    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse AI response as JSON: {e}") from e