from typing import TypedDict

from agents.career_pipeline import run_career_analysis

from langgraph.graph import StateGraph, START, END


class CareerState(TypedDict):
    profile_text: str
    profile: dict
    jobs: list
    priority_skills: list
    training_path: list


def analyze_career(state: CareerState):
    """
    Run the complete career analysis pipeline.

    This includes:
    - Profile parsing
    - Location-based job matching
    - Skill-gap analysis
    - Course recommendations
    - Opportunity ranking
    - Training path
    """

    result = run_career_analysis(
        state["profile_text"]
    )

    return {
        "profile": result["profile"],
        "jobs": result["jobs"],
        "priority_skills": result["priority_skills"],
        "training_path": result["training_path"]
    }


def build_graph():
    """
    Build the Career Agent LangGraph workflow.
    """

    graph = StateGraph(CareerState)

    # Career analysis node
    graph.add_node(
        "career_analysis",
        analyze_career
    )

    # Workflow
    graph.add_edge(
        START,
        "career_analysis"
    )

    graph.add_edge(
        "career_analysis",
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
        "priority_skills": [],
        "training_path": []
    })

    print("\n====================")
    print("PROFILE")
    print("====================")
    print(result["profile"])

    print("\n====================")
    print("PRIORITY SKILLS")
    print("====================")

    for item in result["priority_skills"][:10]:

        print(
            item["skill"],
            "->",
            item["job_count"],
            "jobs"
        )

    print("\n====================")
    print("TRAINING PATH")
    print("====================")

    for item in result["training_path"]:

        print(
            f"Step {item['step']}: "
            f"{item['skill']} -> "
            f"{item['course_name']} "
            f"({item['jobs_unlocked']} jobs)"
        )

    print("\n====================")
    print("JOB RECOMMENDATIONS")
    print("====================")

    for job in result["jobs"]:

        print("\nJob:", job["job_title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Match:", job["match_score"])
        print("Matched:", job["matched_skills"])
        print("Missing:", job["missing_skills"])
        print("Gap:", job["gap_percentage"], "%")

        print("Courses:")

        for course in job["recommended_courses"][:5]:

            print(
                "  -",
                course["course_name"],
                "|",
                course["platform"],
                "|",
                course["opportunity_score"],
                "jobs"
            )