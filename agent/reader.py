import os
import requests
from dotenv import load_dotenv

load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")

def read_url(url: str) -> dict:
    """
    Read the full content of a webpage using Jina AI.
    Returns clean text content from the page.
    """
    print(f"📖 Reading: {url}")

    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Accept": "application/json"
    }

    # Jina reader API - just prepend r.jina.ai to any URL
    jina_url = f"https://r.jina.ai/{url}"

    try:
        response = requests.get(jina_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("data", {}).get("content", "")
            title = data.get("data", {}).get("title", "")
            print(f"✅ Successfully read: {title}")
            return {
                "url": url,
                "title": title,
                "content": content[:3000],  # Limit to 3000 chars
                "success": True
            }
        else:
            print(f"❌ Failed to read: {url}")
            return {"url": url, "content": "", "success": False}

    except Exception as e:
        print(f"❌ Error reading {url}: {e}")
        return {"url": url, "content": "", "success": False}


# Quick test
if __name__ == "__main__":
    result = read_url("https://blogs.nvidia.com/blog/what-is-agentic-ai/")
    print(f"\nTitle: {result['title']}")
    print(f"Content Preview:\n{result['content'][:500]}")