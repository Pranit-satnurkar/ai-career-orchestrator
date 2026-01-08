import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()


def analyze_gap(resume_text, job_description, company_research):
    """
    Compares the resume against the JD and Research to find gaps.
    """
    print("🧠 The Analyst is thinking...")

    # 1. Setup the Brain (GPT-4o-mini is perfect for this)
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # 2. The Prompt (The Instructions)
    template = """
    You are an expert Technical Recruiter and Career Coach. 
    I will give you a Candidate's Resume, a Job Description, and Research about the Company.
    
    YOUR GOAL:
    Identify the "Gap" between the candidate and the job. Be brutally honest but constructive.
    
    INPUTS:
    --- JOB DESCRIPTION ---
    {job_desc}
    
    --- COMPANY RESEARCH ---
    {company_research}
    
    --- CANDIDATE RESUME ---
    {resume}
    
    OUTPUT FORMAT:
    1. **Match Score**: (Give a score out of 100)
    2. **Missing Keywords**: (List specific tools/skills mentioned in JD but missing in Resume)
    3. **Cultural Fit**: (How well does the resume match the company's "Vibe" based on the research?)
    4. **3 Specific Improvements**: (What exactly should I change in the resume to get an interview?)
    
    Provide the analysis now.
    """

    prompt = PromptTemplate.from_template(template)

    # 3. Create the Chain (Prompt -> LLM -> String Output)
    chain = prompt | llm | StrOutputParser()

    # 4. Run it
    result = chain.invoke({
        "resume": resume_text,
        "job_desc": job_description,
        "company_research": company_research
    })

    return result


# --- INTEGRATION TEST ---
if __name__ == "__main__":
    # 1. Import our previous tools
    from pdf_utils import extract_text_from_pdf
    from researcher import get_company_research

    print("--- STARTING FULL PIPELINE ---")

    # Step A: Read the Resume
    print("1. Reading Resume...")
    resume_text = extract_text_from_pdf("resume.pdf")

    # Step B: Read the Job Description
    print("2. Reading Job Description...")
    with open("job_description.txt", "r", encoding="utf-8") as f:
        job_desc = f.read()

    # Step C: Research the Company (This runs the agent we built!)
    print("3. Researching Company (This calls Google)...")
    # HARDCODING Company Name for this test to match the JD
    research_summary = get_company_research("ClinicMind")

    # Step D: Analyze
    print("\n4. Running Gap Analysis...")
    analysis = analyze_gap(resume_text, job_desc, research_summary)

    print("\n\n================ ANALYSIS REPORT ================")
    print(analysis)
    print("=================================================")
