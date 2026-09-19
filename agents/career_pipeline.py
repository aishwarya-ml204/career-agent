import pandas as pd

from agents.profile_parser import parse_profile
from agents.job_matcher import match_jobs
from agents.gap_analyzer import analyze_gap
from agents.course_recommender import recommend_courses

try:
    from agents.opportunity_ranker import rank_missing_skills
except ImportError:
    rank_missing_skills = None

try:
    from agents.training_path import build_training_path
except ImportError:
    build_training_path = None


def is_free_course(cost):
    """Check whether a course is free."""
    if cost is None:
        return False

    return str(cost).strip().lower() in [
        "free",
        "0",
        "0.0",
        "$0",
        "₹0",
    ]


def calculate_training_summary(training_path):
    """Calculate total training hours and whether the path is free."""

    total_hours = 0
    all_free = True

    for course in training_path:
        try:
            hours = float(course.get("duration_hours", 0))
        except (ValueError, TypeError):
            hours = 0

        total_hours += hours

        if not is_free_course(course.get("cost")):
            all_free = False

    return {
        "total_hours": total_hours,
        "all_free": all_free,
    }


def run_career_analysis(profile_text, top_k=5):

    # ========================================================
    # 1. PARSE USER PROFILE
    # ========================================================

    profile = parse_profile(profile_text)

    user_skills = profile.get("skills", [])
    location = profile.get("location", "")

    # ========================================================
    # 2. FIND JOB MATCHES
    # ========================================================

    jobs = match_jobs(
        user_skills=user_skills,
        location=location,
        top_k=top_k,
    )

    # Convert DataFrame to list if necessary
    if isinstance(jobs, pd.DataFrame):

        if jobs.empty:
            jobs_list = []

        else:
            jobs_list = jobs.to_dict("records")

    else:
        jobs_list = jobs or []

    # ========================================================
    # 3. ANALYZE SKILL GAPS
    # ========================================================

    processed_jobs = []

    for job in jobs_list:

        required_skills = job.get("required_skills", "")

        # Handle possible uppercase CSV field
        if not required_skills:
            required_skills = job.get("REQUIRED_SKILLS", "")

        if isinstance(required_skills, str):

            required_skills_list = [
                skill.strip()
                for skill in required_skills.split(",")
                if skill.strip()
            ]

        elif isinstance(required_skills, list):

            required_skills_list = required_skills

        else:

            required_skills_list = []

        try:

            gap = analyze_gap(
                user_skills,
                required_skills_list,
            )

        except Exception:

            user_skill_set = {
                str(skill).lower().strip()
                for skill in user_skills
            }

            required_skill_set = {
                str(skill).lower().strip()
                for skill in required_skills_list
            }

            matched = [
                skill
                for skill in required_skills_list
                if str(skill).lower().strip() in user_skill_set
            ]

            missing = [
                skill
                for skill in required_skills_list
                if str(skill).lower().strip() not in user_skill_set
            ]

            gap = {
                "matched_skills": matched,
                "missing_skills": missing,
                "gap_percentage": (
                    len(missing) / len(required_skills_list) * 100
                    if required_skills_list
                    else 0
                ),
            }

        processed_job = dict(job)

        # Normalize fields used by the UI
        processed_job["job_id"] = job.get(
            "job_id",
            job.get("JOB_ID", ""),
        )

        processed_job["job_title"] = job.get(
            "job_title",
            job.get("JOB_TITLE", ""),
        )

        processed_job["company"] = job.get(
            "company",
            job.get("COMPANY", ""),
        )

        processed_job["location"] = job.get(
            "location",
            job.get("LOCATION", ""),
        )

        processed_job["match_score"] = job.get(
            "match_score",
            0,
        )

        processed_job["matched_skills"] = gap.get(
            "matched_skills",
            [],
        )

        processed_job["missing_skills"] = gap.get(
            "missing_skills",
            [],
        )

        processed_job["gap_percentage"] = gap.get(
            "gap_percentage",
            0,
        )

        processed_jobs.append(processed_job)

    # ========================================================
    # 4. PRIORITY SKILLS
    # ========================================================

    priority_skills = []

    if rank_missing_skills and jobs_list:

        try:
            priority_skills = rank_missing_skills(
                user_skills,
                jobs_list,
            )
        except Exception:
            priority_skills = []

    # ========================================================
    # 5. RECOMMEND COURSES
    # ========================================================

    for job in processed_jobs:

        try:

            courses = recommend_courses(
                job["missing_skills"],
                top_k=5,
            )

        except Exception:

            courses = []

        # Calculate opportunity score
        for course in courses:

            unlocked_jobs = set()

            course_skills = course.get("skills", [])

            if isinstance(course_skills, str):
                course_skills = [
                    skill.strip()
                    for skill in course_skills.split(",")
                    if skill.strip()
                ]

            for matched_job in processed_jobs:

                for missing_skill in matched_job.get(
                    "missing_skills",
                    [],
                ):

                    if any(
                        str(missing_skill).lower().strip()
                        == str(course_skill).lower().strip()
                        for course_skill in course_skills
                    ):
                        unlocked_jobs.add(
                            matched_job["job_id"]
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
                0,
            ),
            reverse=True,
        )

        job["recommended_courses"] = courses

    # ========================================================
    # 6. BUILD TRAINING PATH
    # ========================================================

    training_path = []

    if build_training_path and priority_skills:

        try:

            training_path = build_training_path(
                priority_skills,
                max_steps=5,
            )

        except Exception:

            training_path = []

    # ========================================================
    # 7. TRAINING SUMMARY
    # ========================================================

    training_summary = calculate_training_summary(
        training_path
    )

    # ========================================================
    # 8. FINAL RESULT
    # ========================================================

    return {
        "profile": profile,
        "jobs": processed_jobs,
        "priority_skills": priority_skills,
        "training_path": training_path,
        "training_summary": training_summary,
    }