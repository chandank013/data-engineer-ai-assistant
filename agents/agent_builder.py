# agents/agent_builder.py
# LangChain agent initialisation with all tools

from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq


SYSTEM_PREFIX = """You are an expert AI Data Engineer Assistant.
You help users analyze datasets, query data with Spark SQL, understand ETL pipelines,
and find research information. Always prefer pdf_search tool first if a PDF is available.
Be concise, precise, and technical in your responses."""


def build_agent(api_key: str, tools: list, verbose: bool = False):
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.1-8b-instant",
        streaming=False,
        temperature=0.1,
    )
    return initialize_agent(
        tools, llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=verbose,
        handle_parsing_errors=True,
        agent_kwargs={"prefix": SYSTEM_PREFIX},
    )