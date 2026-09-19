import pandas as pd
import re


JOBS_FILE = "data/job.csv"


def normalize_skill(skill):
    """Convert skill names into a common format."""

    skill = str(skill).lower().strip()

    replacements = {
        "ml": "machine learning",
        "machine-learning": "machine learning",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "js": "javascript",
        "py": "python",
        "scikit learn": "scikit-learn",
        "pytorch or tensorflow": "deep learning",
        "basic deep learning": "deep learning",
        "aws (s3, glue, redshift)": "aws",
        "vector databases": "vector database",
    }

    return replacements.get(skill, skill)


def extract_skills(skill_text):
    """Extract skills while keeping skills inside parentheses together."""

    if not skill_text:
        return []

    text = str(skill_text).strip()

    # Split only on separators that are outside parentheses.
    skills = re.split(
        r",(?=(?:[^()]*\([^()]*\))*[^()]*$)|[;|\n]+",
        text
    )

    return [
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    ]


def calculate_opportunity_scores(jobs):
    """
    Calculate how many job opportunities are associated
    with each missing skill.
    """

    skill_opportunities = {}

    for _, job in jobs.iterrows():

        required_skills = extract_skills(
            job["REQUIRED_SKILLS"]
        )

        for skill in required_skills:

            if skill not in skill_opportunities:
                skill_opportunities[skill] = {
                    "skill": skill,
                    "job_count": 0,
                    "jobs": []
                }

            skill_opportunities[skill]["job_count"] += 1

            skill_opportunities[skill]["jobs"].append(
                job["JOB_TITLE"]
            )

    ranked_skills = list(skill_opportunities.values())

    ranked_skills.sort(
        key=lambda x: x["job_count"],
        reverse=True
    )

    return ranked_skills


def rank_missing_skills(user_skills, jobs):
    """
    Find missing skills across matched jobs and rank them
    according to the number of job opportunities they can unlock.
    """

    user_skills = {
        normalize_skill(skill)
        for skill in user_skills
    }

    missing_skill_data = {}

    for _, job in jobs.iterrows():

        required_skills = extract_skills(
            job["REQUIRED_SKILLS"]
        )

        for skill in required_skills:

            if skill not in user_skills:

                if skill not in missing_skill_data:
                    missing_skill_data[skill] = {
                        "skill": skill,
                        "job_count": 0,
                        "jobs": []
                    }

                missing_skill_data[skill]["job_count"] += 1

                missing_skill_data[skill]["jobs"].append(
                    job["JOB_TITLE"]
                )

    ranked_skills = list(
        missing_skill_data.values()
    )

    ranked_skills.sort(
        key=lambda x: x["job_count"],
        reverse=True
    )

    return ranked_skills


if __name__ == "__main__":

    jobs = pd.read_csv(JOBS_FILE)

    user_skills = [
        "python",
        "sql",
        "machine learning",
        "pandas",
        "numpy"
    ]

    # Use the Bengaluru jobs for this test
    location = "Bengaluru"

    location_jobs = jobs[
        jobs["LOCATION"]
        .fillna("")
        .str.contains(
            location,
            case=False,
            na=False
        )
    ]

    ranked_skills = rank_missing_skills(
        user_skills,
        location_jobs
    )

    print("\n======================================")
    print("OPPORTUNITY-UNLOCKED SKILL RANKING")
    print("======================================")

    for i, item in enumerate(
        ranked_skills,
        start=1
    ):

        print(f"\n{i}. Skill: {item['skill']}")
        print(
            f"   Jobs unlocked: {item['job_count']}"
        )
        print(
            "   Jobs: "
            + ", ".join(item["jobs"])
        )