# llm/groq_llm.py
# Centralised Groq LLM initialisation.

from langchain_groq import ChatGroq


def get_groq_llm(api_key: str, model: str = "llama-3.1-8b-instant", streaming: bool = False) -> ChatGroq:
    """
    Return a configured ChatGroq instance.

    Args:
        api_key:   Groq API key (from user input or env).
        model:     Groq model name. Defaults to llama-3.1-8b-instant.
        streaming: Enable streaming for Streamlit-style callbacks.
    """
    if not api_key:
        raise ValueError("Groq API key is required. Set GROQ_API_KEY or pass via request.")
    return ChatGroq(
        groq_api_key=api_key,
        model_name=model,
        streaming=streaming,
        temperature=0.1,
    )