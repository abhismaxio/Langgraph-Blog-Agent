import os
from typing import List
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()



def _tavily_search(query: str, max_results: int = 5) -> List[dict]:

    if not os.getenv("TAVILY_API_KEY"):
        return []
    
    tool = TavilySearch(max_results=max_results)
    results = tool.invoke({"query": query})
    normalized: List[dict] = []
    for r in results or []:
        normalized.append(
            {
                "title": r.get("title") or "",
                "url": r.get("url") or "",
                "snippet": r.get("content") or r.get("snippet") or "",
                "published_at": r.get("published_date") or r.get("published_at"),
                "source": r.get("source"),
            }
        )
    return normalized
