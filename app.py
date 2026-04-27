import streamlit as st
import os
from dotenv import load_dotenv
from requirement_extractor import extract_requirements
from optimizer import get_tailored_cv
from utils import extract_text_from_pdf

# Load environment variables
load_dotenv()

# Validate API key on startup
if not os.getenv("GOOGLE_API_KEY"):
    st.error("GOOGLE_API_KEY is not set. Please add it to your .env file.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="The Career Alchemist",
    page_icon="🧪",
    layout="wide"
)

# Session state initialization
if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None
if "cv_text" not in st.session_state:
    st.session_state.cv_text = None
if "tailored_cv" not in st.session_state:
    st.session_state.tailored_cv = None
if "jd_text" not in st.session_state:
    st.session_state.jd_text = None

# Sidebar - PM² Governance Info
st.sidebar.title("🧪 Project Info")
st.sidebar.info("""
**Project:** Career Alchemist  
**Phase:** Executing (Sprint 1)  
**Methodology:** PM²  
**Manager:** João Correia
""")

# Main UI Header
st.title("The Career Alchemist: AI Job Search Intelligence")
st.markdown("---")

# Layout: Two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.header("1. Personal Context")
    uploaded_cv = st.file_uploader("Upload your Baseline CV (PDF)", type="pdf")
    if uploaded_cv:
        try:
            cv_text = extract_text_from_pdf(uploaded_cv)
            st.session_state.cv_text = cv_text
            st.success("CV uploaded and parsed successfully.")
        except RuntimeError as e:
            st.error(str(e))

    st.subheader("Tone of Voice")
    st.info("The system will use your predefined Voice Profile for RAG optimization.")

with col2:
    st.header("2. Opportunity Context")
    jd_text = st.text_area("Paste the Job Description here", height=300, placeholder="Copy the JD from LinkedIn/Indeed...")

    if st.button("Analyze Job Requirements"):
        if jd_text.strip():
            if len(jd_text) > 15000:
                st.warning("JD is very long. Consider trimming to the most relevant sections.")
            with st.spinner("Agent 'Analyst' is extracting requirements..."):
                try:
                    st.session_state.jd_analysis = extract_requirements(jd_text)
                    st.session_state.jd_text = jd_text
                except RuntimeError as e:
                    st.error(f"Analysis failed: {e}")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
        else:
            st.warning("Please paste a Job Description to proceed.")

# Display analysis result (persists across reruns via session state)
if st.session_state.jd_analysis:
    st.markdown("---")
    st.header("📋 Job Requirements Analysis")
    st.markdown(st.session_state.jd_analysis)

# CV Optimization section
if st.session_state.jd_analysis and st.session_state.cv_text:
    st.markdown("---")
    st.header("✨ CV Optimizer")
    if st.button("Generate Tailored CV"):
        with st.spinner("Agent 'Optimizer' is rewriting your CV..."):
            try:
                st.session_state.tailored_cv = get_tailored_cv(
                    st.session_state.cv_text,
                    st.session_state.jd_text
                )
            except RuntimeError as e:
                st.error(f"Optimization failed: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

if st.session_state.tailored_cv:
    result = st.session_state.tailored_cv
    st.subheader("Professional Summary")
    st.write(result.get("summary", ""))
    st.subheader("Experience")
    for role in result.get("experience", []):
        st.markdown(f"**{role.get('role')}** — {role.get('company')}")
        for bullet in role.get("bullets", []):
            st.markdown(f"- {bullet}")

# Footer/Status Bar
st.markdown("---")
st.caption("Career Alchemist | Powered by Gemini 2.5 Flash & PM² Framework")