# LangGraph workflow
from typing import TypedDict
from agents.career_pipeline import run_career_analysis
from langgraph.graph import StateGraph, START, END

class CareerState(TypedDict):
    profile_text: str
    profile: dict
    jobs: list


def analyze_career(state: CareerState):
    result = run_career_analysis(state["profile_text"])

    return {
        "profile": result["profile"],
        "jobs": result["jobs"]
    }  
def build_graph():
    graph = StateGraph(CareerState)

    graph.add_node("career_analysis", analyze_career)

    graph.add_edge(START, "career_analysis")
    graph.add_edge("career_analysis", END)

    return graph.compile()  
if __name__ == "__main__":

    app = build_graph()

    test_profile = """
    I am a B.Tech Computer Science student.
    I live in Bengaluru, Karnataka.
    I know Python, SQL, Pandas and NumPy.
    I am interested in machine learning and data science.
    """

    result = app.invoke({
        "profile_text": test_profile,
        "profile": {},
        "jobs": []
    })

    print("\nPROFILE")
    print(result["profile"])

    print("\nJOBS")
    for job in result["jobs"]:
        print(job)