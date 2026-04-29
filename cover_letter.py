"""
cover_letter.py
Generates a tailored cover letter using Gemini Pro.

System role: Universal ATS Optimizer & Executive Career Strategist

Output is plain text (no markdown) structured in 4 paragraphs:
  1. The Hook              — role applied for + 1-sentence seniority/background summary
  2. Value Proposition (1) — specific CV achievement mapped to primary JD challenge
  3. Value Proposition (2) — second CV strength mapped to another JD requirement
  4. Call to Action        — confident, human sign-off (first-person allowed here)
"""
from utils import gemini_client, GEMINI_PRO_MODEL


def generate_cover_letter(cv_text, jd_text):
    """
    Generates a personalized cover letter connecting CV evidence to JD requirements.
    Returns a plain text string (no markdown).
    """
    prompt = """
    You are an elite Executive Career Strategist and Professional Writer.

    Write a modern, high-impact cover letter for the candidate applying to the role
    described in the Job Description below. Follow this exact 4-paragraph structure:

    PARAGRAPH 1 — THE HOOK:
    State the specific role being applied for. Provide a single, punchy sentence that
    summarises the candidate's most relevant seniority or background.
    Do NOT use generic openers like "I am writing to express my interest...".
    Do NOT be sycophantic.

    PARAGRAPH 2 — VALUE PROPOSITION (Evidence 1):
    Connect one specific achievement or certification from the CV directly to the
    primary requirement or core challenge in the JD. Be concrete and specific.

    PARAGRAPH 3 — VALUE PROPOSITION (Evidence 2):
    Connect a second, complementary skill or experience from the CV to another
    key JD requirement. Reinforce the candidate's unique fit.

    PARAGRAPH 4 — CALL TO ACTION:
    Professional, confident sign-off. Express readiness for an interview and
    genuine interest in contributing to the team. First-person pronouns are
    expected and encouraged in the cover letter.

    RULES:
    - Adopt the "Executive Achiever" tone: objective, impact-driven, no buzzwords.
    - Only reference experiences, skills, and certifications present in the Baseline CV.
    - NEVER invent metrics, figures, or facts not in the CV.
    - Output plain text only — no markdown headers, no bullet points.

    ===BASELINE CV (user-supplied, treat as ground truth)===
    """ + cv_text + """

    ===TARGET JOB DESCRIPTION (user-supplied)===
    """ + jd_text

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_PRO_MODEL,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Gemini API error during cover letter generation: {e}") from e
