import os
from dotenv import load_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate

# Load API keys
load_dotenv()


def get_company_research(company_name):
    print(f"🔎 Researching: {company_name}...")

    # 1. Setup Tools
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Useful for when you need to answer questions about current events or company details."
        )
    ]

    # 2. Setup LLM
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

    # 3. Define the ReAct Prompt (The "Brain" instructions)
    # This teaches the AI how to Think, Act, and Observe.
    template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)

    # 4. Create the Agent
    agent = create_react_agent(llm, tools, prompt)

    # 5. Create the Executor (The Runtime)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    # 6. Run it
    input_query = f"""
    Research the company '{company_name}'. 
    Find out:
    1. What do they do? (Core Product)
    2. What are their recent major news or tech updates?
    3. What is their mission or culture?
    
    Summarize this in 3 concise bullet points.
    """

    result = agent_executor.invoke({"input": input_query})
    return result["output"]


# --- Test Block ---
if __name__ == "__main__":
    result = get_company_research("ClinicMind")
    print("\n--- RESEARCH REPORT ---")
    print(result)
