import streamlit as st
import os
from dotenv import load_dotenv
from requirement_extractor import extract_requirements

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
        st.success("CV uploaded — will be used for tailoring in Sprint 2.")

    st.subheader("Tone of Voice")
    st.info("The system will use your predefined Voice Profile for RAG optimization.")

with col2:
    st.header("2. Opportunity Context")
    jd_text = st.text_area("Paste the Job Description here", height=300, placeholder="Copy the JD from LinkedIn/Indeed...")

    if st.button("Analyze Job Requirements"):
        if jd_text.strip():
            with st.spinner("Agent 'Analyst' is extracting requirements..."):
                try:
                    st.session_state.jd_analysis = extract_requirements(jd_text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
        else:
            st.warning("Please paste a Job Description to proceed.")

# Display analysis result (persists across reruns via session state)
if st.session_state.jd_analysis:
    st.markdown("---")
    st.header("📋 Job Requirements Analysis")
    st.markdown(st.session_state.jd_analysis)

# Footer/Status Bar
st.markdown("---")
st.caption("Career Alchemist | Powered by Gemini 2.5 Flash & PM² Framework")