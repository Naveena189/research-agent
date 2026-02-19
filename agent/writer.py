import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def write_report(topic: str, results: list) -> str:
    """
    Generate a structured research report from filtered results.
    Each fact is tied back to its source.
    """
    print(f"\n✍️ Writing report for: {topic}")

    # Build context from results
    context = ""
    for i, r in enumerate(results):
        context += f"\nSource {i+1}: {r.get('title', '')}\n"
        context += f"URL: {r.get('url', '')}\n"
        context += f"Content: {r.get('content', '')[:1000]}\n"
        context += "-" * 40

    prompt = f"""
    You are a research report writer. Using the sources provided, write a 
    comprehensive and well-structured research report on the following topic.
    
    Topic: {topic}
    
    Sources:
    {context}
    
    Your report must:
    1. Have a clear title
    2. Have an introduction
    3. Have 3-4 main sections with headings
    4. Have a conclusion
    5. After each key fact or claim, add the source in brackets like [Source: website.com]
    6. End with a "Sources" section listing all URLs used
    
    Write in a professional, clear, and informative tone.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    
    print("✅ Report generated!")
    return response.content


# Quick test
if __name__ == "__main__":
    # Simulate filtered results
    test_results = [
        {
            "title": "What Is Agentic AI?",
            "url": "https://blogs.nvidia.com/blog/what-is-agentic-ai/",
            "content": "Agentic AI uses sophisticated reasoning and iterative planning to autonomously solve complex multi-step problems. Unlike traditional AI that responds to single prompts, agentic AI can plan, use tools, and complete long horizon tasks."
        },
        {
            "title": "Agentic AI Explained | MIT Sloan",
            "url": "https://mitsloan.mit.edu/ideas-made-to-matter/agentic-ai-explained",
            "content": "Agentic AI systems can perceive their environment, make decisions, and take actions to achieve specific goals. They represent a significant leap beyond generative AI by adding autonomy and goal-directed behavior."
        }
    ]

    report = write_report("What is Agentic AI?", test_results)
    print("\n" + "="*60)
    print(report)