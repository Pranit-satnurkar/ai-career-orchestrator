import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def tailor_resume(resume_text, job_description, gap_analysis):
    """
    Rewrites the resume summary and skills to better match the job.
    """
    print("✍️ The Writer is drafting new content...")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    template = """
    You are an expert Resume Writer and Career Strategist.
    
    YOUR TASK:
    Rewrite the "Professional Summary" and "Skills" sections of the candidate's resume to target the specific Job Description below.
    
    GUIDELINES:
    1. Use the "Gap Analysis" to address weaknesses.
    2. Incorporate specific keywords from the Job Description (e.g., if they want Redshift, mention "Cloud Data Warehousing" or SQL proficiency).
    3. DO NOT LIE. Do not invent experiences the candidate doesn't have. Instead, frame existing skills as "transferable" or "foundational."
    4. Make it sound professional, action-oriented, and confident.
    
    --- INPUT DATA ---
    JOB DESCRIPTION:
    {job_desc}
    
    GAP ANALYSIS FEEDBACK:
    {gap_analysis}
    
    ORIGINAL RESUME CONTENT:
    {resume}
    
    --- OUTPUT ---
    Return the output in Markdown format:
    
    ### 🎯 Tailored Professional Summary
    (New summary here)
    
    ### 🛠 Recommended Skills Section Updates
    (List of skills to add/modify)
    
    ### 🚀 Strategic "Project" Idea
    (Suggest a small project the candidate could do THIS WEEKEND to close the gap, e.g., "Build a QuickSight dashboard using dummy data")
    """

    prompt = PromptTemplate.from_template(template)

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "resume": resume_text,
        "job_desc": job_description,
        "gap_analysis": gap_analysis
    })

    return result


# --- INTEGRATION TEST ---
if __name__ == "__main__":
    # Import tools
    from pdf_utils import extract_text_from_pdf
    from researcher import get_company_research
    from analyst import analyze_gap

    print("--- GENERATING TAILORED CONTENT ---")

    # 1. Load Data (Simulating the pipeline for speed)
    resume_text = extract_text_from_pdf("resume.pdf")
    with open("job_description.txt", "r") as f:
        job_desc = f.read()

    # 2. We need the research and analysis first
    # (In a real app, we pass these variables through. Here we re-run them or hardcode for testing)
    print("...Re-running analysis to get context...")
    research = get_company_research("ClinicMind")
    analysis = analyze_gap(resume_text, job_desc, research)

    # 3. Run the Writer
    tailored_content = tailor_resume(resume_text, job_desc, analysis)

    print("\n\n" + "="*40)
    print(tailored_content)
    print("="*40)
