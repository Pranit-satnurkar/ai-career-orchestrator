import streamlit as st
import os
from pdf_utils import extract_text_from_pdf
from researcher import get_company_research
from analyst import analyze_gap
from writer import tailor_resume

# Page Config
st.set_page_config(page_title="AI Career Orchestrator", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🚀 AI Career Intelligence Orchestrator")
st.markdown("Upload your resume and a job description. The AI will research the company, analyze gaps, and rewrite your resume.")

# --- SIDEBAR: Inputs ---
with st.sidebar:
    st.header("📝 Input Data")

    # 1. Job Description
    job_desc = st.text_area("Paste Job Description Here:", height=300,
                            placeholder="Paste the full JD including Company Name...")

    # 2. Resume Upload
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

    # 3. Company Name (Optional, extracted or manual)
    company_name = st.text_input(
        "Company Name (for Research):", placeholder="e.g. ClinicMind")

    start_btn = st.button("Analyze & Tailor Resume")

# --- MAIN AREA ---
if start_btn:
    if not uploaded_file or not job_desc or not company_name:
        st.error("Please provide a Resume, Job Description, and Company Name!")
    else:
        # Progress Bar
        progress_text = "Starting AI Agents..."
        my_bar = st.progress(0, text=progress_text)

        try:
            # 1. Save uploaded PDF temporarily
            with open("temp_resume.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # --- STEP 1: PARSING ---
            my_bar.progress(20, text="📄 Reading Resume & Job Description...")
            resume_text = extract_text_from_pdf("temp_resume.pdf")

            # --- STEP 2: RESEARCH ---
            my_bar.progress(40, text=f"🔎 Researching {company_name} online...")
            research_summary = get_company_research(company_name)

            # Display Research immediately (Good UX)
            with st.expander("🌍 See Company Research Report", expanded=False):
                st.info(research_summary)

            # --- STEP 3: GAP ANALYSIS ---
            my_bar.progress(70, text="🧠 Identifying Skill Gaps...")
            analysis_result = analyze_gap(
                resume_text, job_desc, research_summary)

            # --- STEP 4: WRITING ---
            my_bar.progress(90, text="✍️ Tailoring Resume Content...")
            tailored_content = tailor_resume(
                resume_text, job_desc, analysis_result)

            my_bar.progress(100, text="✅ Done!")

            # --- DISPLAY RESULTS ---
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Gap Analysis")
                st.markdown(analysis_result)

            with col2:
                st.subheader("✨ Tailored Content")
                st.markdown(tailored_content)

            # Cleanup
            os.remove("temp_resume.pdf")

        except Exception as e:
            st.error(f"An error occurred: {e}")
