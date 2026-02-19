import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def score_relevance(topic: str, content: str) -> float:
    """
    Ask the LLM to score how relevant the content is to the topic.
    Returns a score between 0.0 and 1.0
    """
    prompt = f"""
    Topic: {topic}
    
    Content: {content[:500]}
    
    Rate how relevant this content is to the topic on a scale of 0 to 10.
    Reply with ONLY a number between 0 and 10. Nothing else.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        score = float(response.content.strip()) / 10.0
        return round(score, 2)
    except:
        return 0.0


def filter_results(topic: str, results: list, threshold: float = 0.6) -> list:
    """
    Filter search results by relevance score.
    Only keeps results above the threshold.
    """
    print(f"\n🔎 Filtering {len(results)} results for relevance...")
    
    filtered = []
    for result in results:
        score = score_relevance(topic, result.get("content", ""))
        result["relevance_score"] = score
        print(f"  Score {score} → {result['title'][:60]}")
        
        if score >= threshold:
            filtered.append(result)
    
    print(f"✅ Kept {len(filtered)} relevant results")
    return filtered


# Quick test
if __name__ == "__main__":
    # Simulate results from searcher
    test_results = [
        {
            "title": "What Is Agentic AI?",
            "url": "https://blogs.nvidia.com/blog/what-is-agentic-ai/",
            "content": "Agentic AI uses sophisticated reasoning and iterative planning to solve complex multi-step problems."
        },
        {
            "title": "Best Pizza Recipes 2024",
            "url": "https://example.com/pizza",
            "content": "Here are the best pizza recipes you can make at home with simple ingredients."
        }
    ]
    
    filtered = filter_results("Agentic AI", test_results)
    print(f"\nFinal kept results: {len(filtered)}")
    for r in filtered:
        print(f"  - {r['title']} (score: {r['relevance_score']})")