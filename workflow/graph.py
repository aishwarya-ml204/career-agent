from typing import TypedDict

from agents.career_pipeline import run_career_analysis
from agents.course_recommender import recommend_courses

from langgraph.graph import StateGraph, START, END


class CareerState(TypedDict):
    profile_text: str
    profile: dict
    jobs: list
    courses: list


def analyze_career(state: CareerState):
    """
    Run the existing profile parsing,
    job matching and skill-gap analysis.
    """

    result = run_career_analysis(
        state["profile_text"]
    )

    return {
        "profile": result["profile"],
        "jobs": result["jobs"]
    }


def recommend_training(state: CareerState):
    """
    Collect missing skills from the matched jobs
    and recommend relevant courses.
    """

    all_missing_skills = []

    for job in state["jobs"]:
        all_missing_skills.extend(
            job.get("missing_skills", [])
        )

    # Remove duplicate skills
    missing_skills = list(
        dict.fromkeys(all_missing_skills)
    )

    courses = recommend_courses(
        missing_skills,
        top_k=5
    )

    return {
        "courses": courses
    }


def build_graph():
    """
    Build the complete Career Agent LangGraph workflow.
    """

    graph = StateGraph(CareerState)

    # Nodes
    graph.add_node(
        "career_analysis",
        analyze_career
    )

    graph.add_node(
        "training_recommendation",
        recommend_training
    )

    # Workflow
    graph.add_edge(
        START,
        "career_analysis"
    )

    graph.add_edge(
        "career_analysis",
        "training_recommendation"
    )

    graph.add_edge(
        "training_recommendation",
        END
    )

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
        "jobs": [],
        "courses": []
    })

    print("\nPROFILE")
    print("-------")
    print(result["profile"])

    print("\nJOB RECOMMENDATIONS")
    print("-------------------")

    for job in result["jobs"]:
        print("\nJob:", job["job_title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Match:", job["match_score"])
        print("Missing:", job["missing_skills"])

    print("\nCOURSE RECOMMENDATIONS")
    print("----------------------")

    for course in result["courses"]:
        print("\nCourse:", course["course_name"])
        print("Platform:", course["platform"])
        print("Skills:", course["skills"])
        print("Duration:", course["duration"])
        print("URL:", course["url"])