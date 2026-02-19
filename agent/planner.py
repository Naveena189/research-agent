import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def generate_subquestions(topic: str, num_questions: int = 3) -> list:
    """
    Break a research topic into focused sub-questions.
    """
    print(f"\n🧠 Planning research for: {topic}")

    prompt = f"""
    You are a research planner. Given a research topic, generate {num_questions} 
    focused sub-questions that together would give a comprehensive understanding 
    of the topic.
    
    Topic: {topic}
    
    Reply with ONLY the questions, one per line, numbered.
    No extra text, no explanations.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Parse the numbered questions into a clean list
    lines = response.content.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if line:
            # Remove numbering like "1." or "1)"
            clean = line.lstrip("0123456789.)- ").strip()
            if clean:
                questions.append(clean)
    
    print(f"✅ Generated {len(questions)} sub-questions:")
    for q in questions:
        print(f"  → {q}")
    
    return questions


# Quick test
if __name__ == "__main__":
    questions = generate_subquestions("Impact of AI on healthcare")
    print(f"\nTotal questions: {len(questions)}")