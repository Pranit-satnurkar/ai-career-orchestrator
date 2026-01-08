# 🚀 AI Career Intelligence Orchestrator

An autonomous AI agent system that transforms the job application process. This tool uses a Multi-Agent architecture to research companies, analyze skill gaps, and tailor resumes in real-time.

![App Screenshot](demo_screenshot.png)

## 🏗 Architecture
This project moves beyond simple prompt engineering by creating a multi-step workflow:
1.  **The Parser:** Extracts clean text from PDF resumes using `pypdf`.
2.  **The Researcher (Agent 1):** Uses **LangChain** and **Serper API** to scrape live web data about the target company (recent news, culture, mission).
3.  **The Analyst (Agent 2):** Performs a "Gap Analysis" between the candidate's resume and the Job Description using **GPT-4o**.
4.  **The Writer (Agent 3):** Re-writes specific resume sections to align with the company's needs without hallucinating false skills.
5.  **The Frontend:** A reactive web interface built with **Streamlit**.

## 🛠 Tech Stack
* **Python 3.10+**
* **LangChain** (ReAct Agents, Chains)
* **OpenAI API** (GPT-4o-mini)
* **Serper.dev API** (Google Search Tool)
* **Streamlit** (UI/UX)
* **PyPDF** (Document Processing)

## ⚡ How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Pranit-satnurkar/ai-career-orchestrator.git](https://github.com/Pranit-satnurkar/ai-career-orchestrator.git)
    cd ai-career-orchestrator
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your API keys:
    ```ini
    OPENAI_API_KEY=your_openai_key_here
    SERPER_API_KEY=your_serper_key_here
    ```

4.  **Run the App**
    ```bash
    streamlit run main.py
    ```

## 📂 Project Structure
```text
├── main.py            # Streamlit Interface
├── analyst.py         # Logic for Gap Analysis
├── researcher.py      # Agent for Google Search
├── writer.py          # Agent for Resume Rewriting
├── pdf_utils.py       # PDF Extraction Logic
├── requirements.txt   # Project Dependencies
├── .env               # API Keys (Not uploaded to GitHub)
└── README.md          # Documentation