from agents.profile_parser import parse_profile
from agents.job_matcher import match_jobs
from agents.gap_analyzer import analyze_gap


def run_career_analysis(profile_text, top_k=5):

    # ========================================================
    # 1. PARSE USER PROFILE
    # ========================================================

    profile = parse_profile(profile_text)

    user_skills = profile.get(
        "skills",
        []
    )

    location = profile.get(
        "location",
        ""
    )


    # ========================================================
    # 2. FIND JOB MATCHES
    # ========================================================

    jobs = match_jobs(
        user_skills=user_skills,
        location=location,
        top_k=top_k
    )


    # ========================================================
    # 3. ANALYZE SKILL GAPS FOR EACH JOB
    # ========================================================

    processed_jobs = []


    for job in jobs:

        required_skills = job.get(
            "required_skills",
            ""
        )


        # ----------------------------------------------------
        # Convert required skills to list if necessary
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # Calculate skill gap
        # ----------------------------------------------------

        try:

            gap = analyze_gap(
                user_skills,
                required_skills_list
            )

        except Exception:

            # Safe fallback
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
                if str(skill).lower().strip()
                in user_skill_set
            ]

            missing = [
                skill
                for skill in required_skills_list
                if str(skill).lower().strip()
                not in user_skill_set
            ]

            gap = {
                "matched_skills": matched,
                "missing_skills": missing,
                "gap_percentage": (
                    len(missing)
                    / len(required_skills_list)
                    * 100
                    if required_skills_list
                    else 0
                )
            }


        # ----------------------------------------------------
        # Add gap information to job
        # ----------------------------------------------------

        processed_job = dict(job)


        processed_job["matched_skills"] = gap.get(
            "matched_skills",
            []
        )

        processed_job["missing_skills"] = gap.get(
            "missing_skills",
            []
        )

        processed_job["gap_percentage"] = gap.get(
            "gap_percentage",
            0
        )


        processed_jobs.append(
            processed_job
        )


    # ========================================================
    # 4. FINAL RESULT
    # ========================================================

    return {
        "profile": profile,
        "jobs": processed_jobs
    }