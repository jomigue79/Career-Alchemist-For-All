import os
import pypdf
from google import genai
from dotenv import load_dotenv

load_dotenv()

_api_key = os.getenv("GOOGLE_API_KEY")
if not _api_key:
    raise EnvironmentError("GOOGLE_API_KEY is not set in the environment.")

gemini_client = genai.Client(api_key=_api_key)
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_PRO_MODEL = "gemini-2.5-pro"


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a file-like object (Streamlit UploadedFile).
    """
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        if not text.strip():
            raise ValueError("No text could be extracted from the PDF.")

        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Could not extract text from PDF: {e}") from e