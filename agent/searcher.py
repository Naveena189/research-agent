import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Initialize Tavily client
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search(query: str, max_results: int = 5) -> list:
    """
    Search the web for a given query.
    Returns a list of results with title, url, and content.
    """
    print(f"🔍 Searching for: {query}")
    
    response = client.search(
        query=query,
        max_results=max_results,
        include_raw_content=False
    )
    
    # Extract useful fields from each result
    results = []
    for item in response.get("results", []):
        results.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0)
        })
    
    print(f"✅ Found {len(results)} results")
    return results


# Quick test — only runs when you run this file directly
if __name__ == "__main__":
    results = search("What is Agentic AI?")
    for r in results:
        print(f"\nTitle: {r['title']}")
        print(f"URL: {r['url']}")
        print(f"Score: {r['score']}")
        print(f"Content: {r['content'][:200]}...")