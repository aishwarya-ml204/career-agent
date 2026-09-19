from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.profile_parser import parse_profile
from agents.job_matcher import match_jobs
from agents.gap_analyzer import analyze_gap
from agents.opportunity_ranker import rank_missing_skills
from agents.course_recommender import recommend_courses


class CareerState(TypedDict, total=False):

    # User input
    profile_text: str

    # Profile parser output
    profile: dict
    user_skills: list

    # Job matcher output
    jobs: list

    # Gap analyzer output
    gap_results: list

    # Opportunity ranking output
    priority_skills: list

    # Course recommender output
    training_recommendations: list

    # Final training path
    training_path: list


# ==========================================================
# NODE 1 — PROFILE PARSER
# ==========================================================

def profile_parser_node(state: CareerState):

    print("\n[LangGraph] Profile Parser Agent")

    profile = parse_profile(
        state["profile_text"]
    )

    return {
        "profile": profile,
        "user_skills": profile.get(
            "skills",
            []
        )
    }


# ==========================================================
# NODE 2 — JOB MATCHER
# ==========================================================

def job_matching_node(state: CareerState):

    print("[LangGraph] Job Matching Agent")

    profile = state["profile"]

    jobs_df = match_jobs(
        state["user_skills"],
        location=profile.get("location"),
        top_k=5
    )

    # Convert DataFrame rows to dictionaries
    jobs = []

    for _, job in jobs_df.iterrows():

        jobs.append({
            "JOB_ID": job["JOB_ID"],
            "JOB_TITLE": job["JOB_TITLE"],
            "COMPANY": job["COMPANY"],
            "LOCATION": job["LOCATION"],
            "REQUIRED_SKILLS": job["REQUIRED_SKILLS"],
            "match_score": float(
                job["match_score"]
            )
        })

    return {
        "jobs": jobs
    }


# ==========================================================
# NODE 3 — GAP ANALYZER
# ==========================================================

def gap_analysis_node(state: CareerState):

    print("[LangGraph] Gap Analysis Agent")

    user_skills = state["user_skills"]

    gap_results = []

    for job in state["jobs"]:

        gap = analyze_gap(
            user_skills,
            job["REQUIRED_SKILLS"]
        )

        gap_results.append({

            "job_id": job["JOB_ID"],

            "job_title": job["JOB_TITLE"],

            "company": job["COMPANY"],

            "location": job["LOCATION"],

            "match_score": round(
                job["match_score"],
                3
            ),

            "matched_skills":
                gap["matched_skills"],

            "missing_skills":
                gap["missing_skills"],

            "gap_percentage":
                gap["gap_percentage"]
        })

    return {
        "gap_results": gap_results
    }


# ==========================================================
# NODE 4 — OPPORTUNITY RANKER
# ==========================================================

def opportunity_ranking_node(state: CareerState):

    print("[LangGraph] Opportunity Ranking Agent")

    priority_skills = rank_missing_skills(
        state["user_skills"],
        state["jobs"]
    )

    return {
        "priority_skills": priority_skills
    }


# ==========================================================
# NODE 5 — TRAINING RECOMMENDER
# ==========================================================

def training_recommendation_node(state: CareerState):

    print("[LangGraph] Training Recommendation Agent")

    recommendations = []

    for job in state["gap_results"]:

        courses = recommend_courses(
            job["missing_skills"],
            top_k=5
        )

        recommendations.append({

            "job_id": job["job_id"],

            "job_title": job["job_title"],

            "courses": courses
        })

    return {
        "training_recommendations":
            recommendations
    }


# ==========================================================
# NODE 6 — TRAINING PATH
# ==========================================================

def training_path_node(state: CareerState):

    print("[LangGraph] Training Path Agent")

    training_path = []

    priority_skills = (
        state.get(
            "priority_skills",
            []
        )
    )

    recommendations = (
        state.get(
            "training_recommendations",
            []
        )
    )

    # Build course lookup
    course_lookup = {}

    for job_data in recommendations:

        for course in job_data["courses"]:

            course_name = course[
                "course_name"
            ]

            if course_name not in course_lookup:

                course_lookup[
                    course_name
                ] = course

    step = 1

    # Use priority skills to construct
    # a concise learning path.
    for priority in priority_skills[:5]:

        skill = priority["skill"]

        selected_course = None

        for course in course_lookup.values():

            course_skills = [
                str(s).lower()
                for s in course.get(
                    "skills",
                    []
                )
            ]

            if skill.lower() in course_skills:

                selected_course = course

                break

        if selected_course is None:

            continue

        training_path.append({

            "step": step,

            "skill": skill,

            "course_name":
                selected_course[
                    "course_name"
                ],

            "platform":
                selected_course[
                    "platform"
                ],

            "level":
                selected_course.get(
                    "level",
                    "N/A"
                ),

            "duration":
                selected_course.get(
                    "duration",
                    "N/A"
                ),

            "url":
                selected_course.get(
                    "url",
                    ""
                ),

            "jobs_unlocked":
                priority.get(
                    "job_count",
                    0
                )
        })

        step += 1

    return {
        "training_path": training_path
    }


# ==========================================================
# BUILD LANGGRAPH
# ==========================================================

def build_graph():

    graph = StateGraph(
        CareerState
    )

    # -----------------------------
    # Nodes
    # -----------------------------

    graph.add_node(
        "profile_parser",
        profile_parser_node
    )

    graph.add_node(
        "job_matching",
        job_matching_node
    )

    graph.add_node(
        "gap_analysis",
        gap_analysis_node
    )

    graph.add_node(
        "opportunity_ranking",
        opportunity_ranking_node
    )

    graph.add_node(
        "training_recommendation",
        training_recommendation_node
    )

    graph.add_node(
        "training_path",
        training_path_node
    )

    # -----------------------------
    # Edges
    # -----------------------------

    graph.add_edge(
        START,
        "profile_parser"
    )

    graph.add_edge(
        "profile_parser",
        "job_matching"
    )

    graph.add_edge(
        "job_matching",
        "gap_analysis"
    )

    graph.add_edge(
        "gap_analysis",
        "opportunity_ranking"
    )

    graph.add_edge(
        "opportunity_ranking",
        "training_recommendation"
    )

    graph.add_edge(
        "training_recommendation",
        "training_path"
    )

    graph.add_edge(
        "training_path",
        END
    )

    return graph.compile()


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    app = build_graph()

    profile_text = """
    I am a B.Tech Computer Science student.
    I live in Bengaluru, Karnataka.
    I know Python, SQL, Pandas and NumPy.
    I am interested in machine learning and data science.
    """

    result = app.invoke({

        "profile_text":
            profile_text

    })

    print("\n")
    print("=" * 50)
    print("LANGGRAPH CAREER AGENT")
    print("=" * 50)

    print("\nPROFILE")
    print("-------")

    print(
        result["profile"]
    )

    print("\nPRIORITY SKILLS")
    print("---------------")

    for item in result.get(
        "priority_skills",
        []
    )[:10]:

        print(
            f"{item['skill']} "
            f"-> {item['job_count']} jobs"
        )

    print("\nTRAINING PATH")
    print("-------------")

    for item in result.get(
        "training_path",
        []
    ):

        print(
            f"Step {item['step']}: "
            f"{item['skill']} -> "
            f"{item['course_name']} "
            f"({item['jobs_unlocked']} jobs)"
        )

    print("\nJOB GAP ANALYSIS")
    print("----------------")

    for job in result.get(
        "gap_results",
        []
    ):

        print(
            f"\n{job['job_title']} "
            f"({job['company']})"
        )

        print(
            "Match:",
            job["match_score"]
        )

        print(
            "Missing:",
            job["missing_skills"]
        )

        print(
            "Gap:",
            job["gap_percentage"],
            "%"
        )