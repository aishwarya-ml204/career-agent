import pandas as pd

from agents.profile_parser import parse_profile
from agents.job_matcher import match_jobs
from agents.gap_analyzer import analyze_gap
from agents.course_recommender import recommend_courses
from agents.opportunity_ranker import rank_missing_skills
from agents.training_path import build_training_path


def is_free_course(cost):
    """
    Check whether a course is free.
    """
    if cost is None:
        return False

    return str(cost).strip().lower() in [
        "free",
        "0",
        "0.0",
        "$0",
        "₹0"
    ]


def calculate_training_summary(training_path):
    """
    Calculate total training hours and
    identify whether the complete path is free.
    """

    total_hours = 0
    all_free = True

    for course in training_path:

        # Convert duration hours safely
        try:
            hours = float(course["duration_hours"])
        except (ValueError, TypeError):
            hours = 0

        total_hours += hours

        if not is_free_course(course["cost"]):
            all_free = False

    return {
        "total_hours": total_hours,
        "all_free": all_free
    }


def run_career_analysis(profile_text, top_k=5):

    # Step 1: Parse user profile
    profile = parse_profile(profile_text)

    user_skills = profile["skills"]

    print(
        "Detected location:",
        profile.get("location")
    )

    # Step 2: Find matching jobs
    jobs = match_jobs(
        user_skills,
        location=profile.get("location"),
        top_k=top_k
    )

    if jobs.empty:
        return {
            "profile": profile,
            "jobs": [],
            "priority_skills": [],
            "training_path": [],
            "training_summary": {
                "total_hours": 0,
                "all_free": True
            }
        }

    # Step 3: Analyze skill gaps
    results = []

    for _, job in jobs.iterrows():

        gap = analyze_gap(
            user_skills,
            job["REQUIRED_SKILLS"]
        )

        results.append({
            "job_id": job["JOB_ID"],
            "job_title": job["JOB_TITLE"],
            "company": job["COMPANY"],
            "location": job["LOCATION"],
            "match_score": round(
                float(job["match_score"]),
                3
            ),
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
            "gap_percentage": gap["gap_percentage"]
        })

    # Step 4: Rank missing skills by opportunity
    priority_skills = rank_missing_skills(
        user_skills,
        jobs
    )

    # Step 5: Recommend courses for each job
    for job in results:

        courses = recommend_courses(
            job["missing_skills"],
            top_k=5
        )

        for course in courses:

            unlocked_jobs = set()

            for matched_job in results:

                for missing_skill in matched_job["missing_skills"]:

                    if missing_skill in course["skills"]:

                        unlocked_jobs.add(
                            matched_job["job_id"]
                        )

                        break

            course["jobs_unlocked"] = len(
                unlocked_jobs
            )

            course["opportunity_score"] = len(
                unlocked_jobs
            )

        courses.sort(
            key=lambda x: x["opportunity_score"],
            reverse=True
        )

        job["recommended_courses"] = courses

    # Step 6: Build overall training path
    training_path = build_training_path(
        priority_skills,
        max_steps=5
    )

    # Step 7: Calculate time-to-ready information
    training_summary = calculate_training_summary(
        training_path
    )

    # Final result
    return {
        "profile": profile,
        "jobs": results,
        "priority_skills": priority_skills,
        "training_path": training_path,
        "training_summary": training_summary
    }


if __name__ == "__main__":

    profile_text = """
    I am a B.Tech Computer Science student.
    I live in Bengaluru, Karnataka.
    I know Python, SQL, Pandas and NumPy.
    I am interested in machine learning and data science.
    """

    result = run_career_analysis(
        profile_text
    )

    print("\nUSER SKILLS")
    print("-----------")

    print(
        result["profile"]["skills"]
    )

    print("\nPRIORITY SKILLS")
    print("---------------")

    for i, skill in enumerate(
        result["priority_skills"][:10],
        start=1
    ):

        print(
            f"{i}. {skill['skill']} "
            f"-> {skill['job_count']} jobs"
        )

    print("\nTRAINING PATH")
    print("-------------")

    for item in result["training_path"]:

        print(
            f"\nStep {item['step']}: "
            f"{item['skill']}"
        )

        print(
            "Course:",
            item["course_name"]
        )

        print(
            "Platform:",
            item["platform"]
        )

        print(
            "Level:",
            item["level"]
        )

        print(
            "Duration:",
            item["duration"]
        )

        print(
            "Duration Hours:",
            item["duration_hours"]
        )

        print(
            "Cost:",
            item["cost"]
        )

        print(
            "Jobs potentially unlocked:",
            item["jobs_unlocked"]
        )

    print("\nTRAINING SUMMARY")
    print("----------------")

    print(
        "Total Training Hours:",
        result["training_summary"]["total_hours"]
    )

    print(
        "Entire Path Free:",
        result["training_summary"]["all_free"]
    )

    print("\nJOB RECOMMENDATIONS")
    print("-------------------")

    for job in result["jobs"]:

        print("\nJob:", job["job_title"])
        print("Company:", job["company"])
        print("Location:", job["location"])

        print(
            "Match Score:",
            job["match_score"]
        )

        print(
            "Missing Skills:",
            job["missing_skills"]
        )

        print(
            "Gap:",
            job["gap_percentage"],
            "%"
        )

        print("Recommended Courses:")

        for course in job["recommended_courses"]:

            print(
                "  -",
                course["course_name"],
                "|",
                course["platform"],
                "| Duration:",
                course["duration"],
                "| Hours:",
                course["duration_hours"],
                "| Cost:",
                course["cost"],
                "| Opportunity:",
                course["opportunity_score"],
                "jobs"
            )