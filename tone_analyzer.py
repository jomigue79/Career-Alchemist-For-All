import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY is not set in the environment.")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"

def extract_voice_parameters(text_sample):
    prompt = f"""
    Analyze the following professional text sample. 
    Extract the 'writing voice' parameters including:
    1. Average sentence length.
    2. Common power verbs used.
    3. Technical vs. General vocabulary ratio.
    4. Level of formality (1-10).
    
    Output the result in valid JSON format with no additional text or markdown.
    
    SAMPLE:
    {text_sample}
    """

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    raw = response.text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    return json.loads(raw)

if __name__ == "__main__":
    sample_cv_text = """
    Certified Project Manager with 4+ years of experience in the video game industry. 
    Adept in Agile methodologies, cross-functional team coordination, and digital production pipelines. 
    Proven track record in entrepreneurship, team leadership, and scalable project execution.
    """

    print("Analyzing voice profile...")
    try:
        analysis = extract_voice_parameters(sample_cv_text)
        print(json.dumps(analysis, indent=2))

        os.makedirs("data", exist_ok=True)
        with open("data/voice_params.json", "w") as f:
            json.dump(analysis, f, indent=2)
        print("Saved to data/voice_params.json")
    except json.JSONDecodeError as e:
        print(f"Failed to parse API response as JSON: {e}")
    except Exception as e:
        print(f"Error: {e}")