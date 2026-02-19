import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()

# Import our components
from agent.planner import generate_subquestions
from agent.searcher import search
from agent.reader import read_url
from agent.filter import filter_results
from agent.writer import write_report

# Define the state — this is what gets passed between each step
class ResearchState(TypedDict):
    topic: str
    subquestions: list
    raw_results: list
    filtered_results: list
    report: str

# --- Node Functions ---
# Each function below is one "node" in our agent graph

def plan_node(state: ResearchState) -> ResearchState:
    """Break topic into sub-questions"""
    questions = generate_subquestions(state["topic"])
    return {"subquestions": questions}

def search_node(state: ResearchState) -> ResearchState:
    """Search the web for each sub-question"""
    all_results = []
    for question in state["subquestions"]:
        results = search(question, max_results=3)
        all_results.extend(results)
    
    # Remove duplicates by URL
    seen = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique_results.append(r)
    
    return {"raw_results": unique_results}

def read_node(state: ResearchState) -> ResearchState:
    """Read full content of each result"""
    enriched = []
    for result in state["raw_results"][:6]:  # Limit to 6 to save API calls
        full_content = read_url(result["url"])
        if full_content["success"]:
            result["content"] = full_content["content"]
        enriched.append(result)
    return {"raw_results": enriched}

def filter_node(state: ResearchState) -> ResearchState:
    """Filter results by relevance"""
    filtered = filter_results(state["topic"], state["raw_results"])
    return {"filtered_results": filtered}

def write_node(state: ResearchState) -> ResearchState:
    """Write the final report"""
    report = write_report(state["topic"], state["filtered_results"])
    return {"report": report}

# --- Build the Graph ---
def build_pipeline():
    graph = StateGraph(ResearchState)
    
    # Add nodes
    graph.add_node("planner", plan_node)
    graph.add_node("searcher", search_node)
    graph.add_node("reader", read_node)
    graph.add_node("filter", filter_node)
    graph.add_node("writer", write_node)
    
    # Connect nodes in order
    graph.set_entry_point("planner")
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher", "reader")
    graph.add_edge("reader", "filter")
    graph.add_edge("filter", "writer")
    graph.add_edge("writer", END)
    
    return graph.compile()

# Quick test
if __name__ == "__main__":
    pipeline = build_pipeline()
    
    result = pipeline.invoke({
        "topic": "What is Agentic AI?",
        "subquestions": [],
        "raw_results": [],
        "filtered_results": [],
        "report": ""
    })
    
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)
    print(result["report"])