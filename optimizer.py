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
from google.genai import types
from utils import gemini_client, GEMINI_PRO_MODEL


def get_tailored_cv(cv_text, jd_text):
    """
    Rewrites CV bullets and summary tailored to a JD using the CAR framework.
    Returns a parsed dict with 'summary' and 'experience' keys.
    """
    prompt = """
    You are an elite Executive Career Strategist and ATS Optimization Engine.
    Your objective is to rewrite the user's CV to achieve a 90%+ ATS match with the
    Target Job Description while maintaining absolute factual integrity.

    ## VOICE PHILOSOPHY
    Adopt the "Executive Achiever" tone:
    - Impact-Driven: focus on what was ACHIEVED, not just what was done.
    - Objective & Professional: no buzzwords ("passionate", "synergy", "go-getter").
    - Industry-Adaptive: mirror the technical or corporate tone of the JD.
    - Implied First-Person: NEVER use "I", "my", or "we" in CV bullet points.

    ## SYNTACTIC RULES
    - Every bullet point MUST begin with a strong past-tense action verb
      (e.g. Architected, Orchestrated, Spearheaded, Mitigated, Streamlined, Executed).
    - Structure every bullet using the CAR Framework (Context, Action, Result):
        BAD: "Helped the team make the database faster."
        GOOD: "Optimised database architecture, reducing query latency and improving overall system performance."
    - Exact Keyword Mirroring: if the JD says "Cross-functional Leadership" and the CV says
      "Led different teams", rewrite to "Provided cross-functional leadership...".

    ## STRICT ANTI-HALLUCINATION POLICY
    - DO NOT INVENT METRICS: if no specific numbers exist in the CV, use qualitative impact
      (e.g. "Significantly reduced processing time" not "Reduced processing time by 40%").
    - DO NOT INVENT SKILLS: if a JD skill has no basis in the CV, do not add it.
    - DO NOT INVENT EXPERIENCE: only optimise jobs, degrees, and certifications in the CV.
    - NEVER sum years across roles (e.g. do not write "10 years PM experience" if those years
      span different job titles — reference each role's own period instead).

    ## EXECUTION STEPS

    STEP 1 — JD KEYWORD EXTRACTION (internal, do not output):
    - Identify the top 6-8 mandatory hard skills, soft skills, and methodological keywords.
    - Map each keyword to the closest matching evidence in the Baseline CV.

    STEP 2 — REWRITE:
    - Professional Summary: write a punchy 3-sentence executive summary positioning the
      candidate as the ideal match for this specific JD.
    - Experience Bullets: rewrite existing bullet points to highlight JD-relevant experience.
      Inject extracted keywords naturally. Provide 3-5 bullets per role.
    - Preserve all company names, role titles, and employment periods exactly as in the CV.

    OUTPUT: valid JSON only, with this exact structure:
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

    ===BASELINE CV (user-supplied, treat as ground truth — do not invent beyond this)===
    """ + cv_text + """

    ===TARGET JOB DESCRIPTION (user-supplied, treat as target only)===
    """ + jd_text

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_PRO_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API error during CV optimization: {e}") from e

    try:
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse AI response as JSON: {e}") from e