import sys
from pathlib import Path
from typing import TypedDict
import os
import json

# Make project root visible to Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from langgraph.graph import StateGraph, START, END

from agents.profile_parser import parse_profile
from agents.job_matcher import match_jobs
from agents.gap_analyzer import analyze_gap
from agents.opportunity_ranker import rank_missing_skills
from agents.course_recommender import recommend_courses
from agents.training_path import build_training_path


class CareerState(TypedDict, total=False):
    profile_text: str
    profile: dict
    jobs: list
    priority_skills: list
    llm_analysis: dict
    training_path: list
    training_summary: dict


# -----------------------------
# 1. PROFILE PARSER
# -----------------------------

def profile_parser_node(state):

    profile = parse_profile(
        state["profile_text"]
    )

    print("\n[1] Profile parsed")

    return {
        "profile": profile
    }


# -----------------------------
# 2. JOB MATCHING
# -----------------------------

def job_matching_node(state):

    profile = state["profile"]

    matched_jobs = match_jobs(
        profile.get("skills", []),
        location=profile.get("location"),
        top_k=5
    )

    # Current job_matcher.py returns a list.
    # Keep compatibility if it ever returns a DataFrame.
    if isinstance(matched_jobs, pd.DataFrame):

        jobs = matched_jobs.to_dict(
            orient="records"
        )

    else:

        jobs = matched_jobs or []

    # Add the original CSV-style field names
    # required by the existing LangGraph nodes.
    normalized_jobs = []

    for job in jobs:

        normalized_job = dict(job)

        normalized_job["JOB_ID"] = job.get(
            "JOB_ID",
            job.get("job_id", "")
        )

        normalized_job["JOB_TITLE"] = job.get(
            "JOB_TITLE",
            job.get("job_title", "")
        )

        normalized_job["COMPANY"] = job.get(
            "COMPANY",
            job.get("company", "")
        )

        normalized_job["LOCATION"] = job.get(
            "LOCATION",
            job.get("location", "")
        )

        normalized_job["REQUIRED_SKILLS"] = job.get(
            "REQUIRED_SKILLS",
            job.get("required_skills", "")
        )

        normalized_job["JOB_DESCRIPTION"] = job.get(
            "JOB_DESCRIPTION",
            job.get("job_description", "")
        )

        normalized_job["SOURCE_URL"] = job.get(
            "SOURCE_URL",
            job.get("source_url", "")
        )

        normalized_jobs.append(
            normalized_job
        )

    print(
        f"[2] Jobs matched: {len(normalized_jobs)}"
    )

    return {
        "jobs": normalized_jobs
    }


# -----------------------------
# 3. GAP ANALYSIS
# -----------------------------

def gap_analysis_node(state):

    profile = state["profile"]

    user_skills = profile.get(
        "skills",
        []
    )

    analyzed_jobs = []

    for job in state.get("jobs", []):

        gap = analyze_gap(
            user_skills,
            job["REQUIRED_SKILLS"]
        )

        analyzed_jobs.append({
    # Keep original CSV column names
    # These are used by the ranking logic
    "JOB_ID": job["JOB_ID"],
    "JOB_TITLE": job["JOB_TITLE"],
    "COMPANY": job["COMPANY"],
    "LOCATION": job["LOCATION"],
    "REQUIRED_SKILLS": job["REQUIRED_SKILLS"],

    # Lowercase fields used by Streamlit UI
    "job_id": job["JOB_ID"],
    "job_title": job["JOB_TITLE"],
    "company": job["COMPANY"],
    "location": job["LOCATION"],
    "required_skills": job["REQUIRED_SKILLS"],

    # Matching score
    "match_score": round(
        float(job["match_score"]),
        3
    ),

    # Gap analysis
    "matched_skills": gap["matched_skills"],
    "missing_skills": gap["missing_skills"],
    "gap_percentage": gap["gap_percentage"]
})

    print("[3] Gap analysis complete")

    return {
        "jobs": analyzed_jobs
    }


# -----------------------------
# 4. OPPORTUNITY RANKING
# -----------------------------

def opportunity_ranking_node(state):

    profile = state["profile"]

    user_skills = profile.get(
        "skills",
        []
    )

    jobs_df = pd.DataFrame(
        state.get("jobs", [])
    )

    if jobs_df.empty:

        return {
            "priority_skills": []
        }

    priority_skills = rank_missing_skills(
        user_skills,
        jobs_df
    )

    print("[4] Priority skills calculated")

    return {
        "priority_skills": priority_skills
    }


# -----------------------------
# 5. LLM REASONING
# -----------------------------
def llm_reasoning_node(state):

    jobs = state.get(
        "jobs",
        []
    )

    priority_skills = state.get(
        "priority_skills",
        []
    )

    profile = state.get(
        "profile",
        {}
    )

    # ---------------------------------------
    # No jobs
    # ---------------------------------------

    if not jobs:

        return {
            "llm_analysis": {
                "summary": "No matching jobs were found.",
                "learning_strategy": "Try expanding the job location.",
                "priority_explanations": [],
                "job_insights": []
            }
        }

    # ---------------------------------------
    # Check Gemini API key
    # ---------------------------------------

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        print(
            "[5] GEMINI_API_KEY not found"
        )

        return {
            "llm_analysis": {
                "summary": (
                    f"Your profile was matched against "
                    f"{len(jobs)} jobs."
                ),
                "learning_strategy": (
                    "Focus on skills that unlock "
                    "multiple jobs."
                ),
                "priority_explanations": [],
                "job_insights": []
            }
        }

    # ---------------------------------------
    # Gemini
    # ---------------------------------------

    from google import genai

    client = genai.Client(
        api_key=api_key
    )

    # ---------------------------------------
    # Prompt
    # ---------------------------------------

    prompt = f"""
You are the reasoning layer of a Career Agent.

Analyze this candidate using ONLY the information provided below.

Do not invent:
- jobs
- companies
- skills
- courses
- scores

Explain the existing analysis clearly for the candidate.

CANDIDATE:
{json.dumps(profile, indent=2)}

MATCHED JOBS:
{json.dumps(jobs, indent=2)}

PRIORITY SKILLS:
{json.dumps(priority_skills, indent=2)}

Return ONLY valid JSON in exactly this format:

{{
    "summary": "2-4 sentence career summary",

    "priority_explanations": [
        {{
            "skill": "skill name",
            "explanation": "why this skill matters"
        }}
    ],

    "job_insights": [
        {{
            "job_id": "job id",
            "explanation": "why this job is relevant"
        }}
    ],

    "learning_strategy": "what the candidate should learn first and why"
}}

Do not use markdown.
Return only JSON.
"""

    import time

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            content = response.text.strip()

            if content.startswith("```"):
                content = (
                    content
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            analysis = json.loads(content)

            print("[5] Gemini reasoning complete")

            return {
                "llm_analysis": analysis
            }

        except Exception as e:

            print(
                f"[5] Gemini attempt "
                f"{attempt + 1}/{max_retries} failed: {e}"
            )

            if attempt < max_retries - 1:
                time.sleep(5)

    print("[5] Gemini failed after all retries")

    return {
        "llm_analysis": {
            "summary": (
                "Gemini was temporarily unavailable. "
                "The job matching and skill-gap analysis "
                "were completed successfully."
            ),
            "learning_strategy": (
                "Focus on the highest-priority missing "
                "skills identified across your target jobs."
            ),
            "priority_explanations": [],
            "job_insights": []
        }
    }
# -----------------------------
# 6. COURSE RECOMMENDATION
# -----------------------------

def course_recommendation_node(state):

    jobs = state.get(
        "jobs",
        []
    )

    updated_jobs = []

    for job in jobs:

        courses = recommend_courses(
            job["missing_skills"],
            top_k=5
        )

        for course in courses:

            unlocked_jobs = set()

            for other_job in jobs:

                for skill in other_job["missing_skills"]:

                    if skill in course["skills"]:

                        unlocked_jobs.add(
                            other_job["JOB_ID"]
                        )

            course["jobs_unlocked"] = len(
                unlocked_jobs
            )

            course["opportunity_score"] = len(
                unlocked_jobs
            )

        courses.sort(
            key=lambda x: x.get(
                "opportunity_score",
                0
            ),
            reverse=True
        )

        new_job = dict(job)

        new_job["recommended_courses"] = courses

        updated_jobs.append(
            new_job
        )

    print("[6] Courses recommended")

    return {
        "jobs": updated_jobs
    }


# -----------------------------
# 7. TRAINING PATH
# -----------------------------

def training_path_node(state):

    priority_skills = state.get(
        "priority_skills",
        []
    )

    training_path = build_training_path(
        priority_skills,
        max_steps=5
    )

    total_hours = 0
    all_free = True

    for course in training_path:

        try:
            total_hours += float(
                course.get(
                    "duration_hours",
                    0
                )
            )
        except:
            pass

        cost = str(
            course.get(
                "cost",
                ""
            )
        ).lower().strip()

        if cost not in [
            "free",
            "0",
            "0.0",
            "$0",
            "₹0"
        ]:

            all_free = False

    print("[7] Training path created")

    return {
        "training_path": training_path,
        "training_summary": {
            "total_hours": total_hours,
            "all_free": all_free
        }
    }


# -----------------------------
# BUILD GRAPH
# -----------------------------

def build_graph():

    graph = StateGraph(
        CareerState
    )

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
        "llm_reasoning",
        llm_reasoning_node
    )

    graph.add_node(
        "course_recommendation",
        course_recommendation_node
    )

    graph.add_node(
        "training_path",
        training_path_node
    )

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
        "llm_reasoning"
    )

    graph.add_edge(
        "llm_reasoning",
        "course_recommendation"
    )

    graph.add_edge(
        "course_recommendation",
        "training_path"
    )

    graph.add_edge(
        "training_path",
        END
    )

    return graph.compile()


# -----------------------------
# TEST
# -----------------------------

if __name__ == "__main__":

    app = build_graph()

    test_profile = """
    I am a B.Tech Computer Science student.
    I live in Bengaluru, Karnataka.
    I know Python, SQL, Pandas and NumPy.
    I am interested in machine learning and data science.
    """

    result = app.invoke({
        "profile_text": test_profile
    })

    print("\n====================")
    print("PROFILE")
    print("====================")

    print(
        result.get("profile")
    )

    print("\n====================")
    print("PRIORITY SKILLS")
    print("====================")

    for item in result.get(
        "priority_skills",
        []
    )[:10]:

        print(
            item.get("skill"),
            "->",
            item.get("job_count"),
            "jobs"
        )

    print("\n====================")
    print("LLM ANALYSIS")
    print("====================")

    print(
        json.dumps(
            result.get(
                "llm_analysis",
                {}
            ),
            indent=2
        )
    )

    print("\n====================")
    print("TRAINING PATH")
    print("====================")

    for item in result.get(
        "training_path",
        []
    ):

        print(
            item.get("skill"),
            "->",
            item.get("course_name")
        )

    print("\n====================")
    print("JOBS")
    print("====================")

    for job in result.get(
        "jobs",
        []
    ):

        print(
            job["JOB_TITLE"],
            "|",
            job["COMPANY"],
            "|",
            job["match_score"]
        )

        print(
            "Missing:",
            job["missing_skills"]
        )