import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY is not set in the environment.")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"

def extract_requirements(jd_text):
    prompt = f"""
    Act as an expert ATS (Applicant Tracking System) and Technical Recruiter.
    Analyze the following Job Description and extract:
    1. Top 10 Hard Skills (Keywords).
    2. Top 5 Soft Skills.
    3. Minimum Qualifications (Years of experience, certifications).
    4. "Critical Success Factors" (What does this role actually care about?).

    Output in a clear Markdown format.

    JOB DESCRIPTION:
    {jd_text}
    """

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text

if __name__ == "__main__":
    target_path = "data/targets/"

    if not os.path.exists(target_path):
        print(f"Please create the {target_path} folder and add job description .txt files.")
    else:
        for filename in os.listdir(target_path):
            if filename.endswith(".txt"):
                print(f"Processing {filename}...")
                try:
                    with open(os.path.join(target_path, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                    analysis = extract_requirements(content)
                    output_name = f"analysis_{filename.replace('.txt', '.md')}"
                    with open(os.path.join(target_path, output_name), 'w', encoding='utf-8') as out:
                        out.write(analysis)
                    print(f"Analysis saved to {output_name}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")