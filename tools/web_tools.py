# tools/web_tools.py
# Web research tools with DuckDuckGo rate-limit resilience.
# Uses WikipediaAPIWrapper + ArxivAPIWrapper as primary sources,
# DuckDuckGo as tertiary with automatic retry/backoff.

from __future__ import annotations
import time
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain.tools import Tool


# ─── Resilient DuckDuckGo wrapper ─────────────────────────────────────────────

def _ddg_search_with_retry(query: str, max_retries: int = 3, delay: float = 2.0) -> str:
    """
    DuckDuckGo search with exponential-backoff retry on rate-limit (202) errors.
    Falls back to a Wikipedia search if DDG keeps failing.
    """
    for attempt in range(max_retries):
        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            result = DuckDuckGoSearchRun().run(query)
            if result and "Ratelimit" not in result:
                return result
            # Got rate-limited — wait and retry
            wait = delay * (2 ** attempt)
            time.sleep(wait)
        except Exception as e:
            err = str(e)
            if "202" in err or "Ratelimit" in err or "ratelimit" in err.lower():
                wait = delay * (2 ** attempt)
                time.sleep(wait)
            else:
                break

    # Final fallback: Wikipedia search
    try:
        wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=800)
        return f"[DDG unavailable — Wikipedia fallback]\n{wiki.run(query)}"
    except Exception:
        return f"Search temporarily unavailable. Try rephrasing or ask about a specific paper/topic."


def _make_ddg_tool() -> Tool:
    return Tool(
        name="web_search",
        func=_ddg_search_with_retry,
        description=(
            "Search the web for current information. Use for recent events, "
            "documentation, tutorials, or anything not covered by ArXiv or Wikipedia. "
            "Falls back to Wikipedia if DuckDuckGo is rate-limited."
        ),
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def get_web_tools() -> list:
    """
    Return [arxiv, wikipedia, web_search] LangChain tools.
    DuckDuckGo has rate-limit resilience built in.
    """
    arxiv = ArxivQueryRun(
        api_wrapper=ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=600)
    )
    wikipedia = WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=600)
    )
    web_search = _make_ddg_tool()
    return [arxiv, wikipedia, web_search]