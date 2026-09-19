import pandas as pd
import re


COURSES_FILE = "data/courses.csv"


def normalize_skill(skill):
    """Normalize skill names for comparison."""

    skill = str(skill).lower().strip()

    replacements = {
        "ml": "machine learning",
        "machine-learning": "machine learning",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "js": "javascript",
        "py": "python",
    }

    return replacements.get(skill, skill)


def split_skills(skill_text):
    """Convert a course skill field into individual skills."""

    if not skill_text:
        return []

    skills = re.split(r"[,;|/\n]+", str(skill_text))

    return [
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    ]


def recommend_courses(missing_skills, top_k=5):
    """
    Recommend courses based on the candidate's missing skills.
    """

    if not missing_skills:
        return []

    courses = pd.read_csv(COURSES_FILE)

    missing = {
        normalize_skill(skill)
        for skill in missing_skills
    }

    recommendations = []

    for _, course in courses.iterrows():

        course_skills = split_skills(course["skills"])

        matched_skills = [
            skill
            for skill in course_skills
            if skill in missing
        ]

        if matched_skills:

            recommendations.append({
                "course_id": course["course_id"],
                "course_name": course["course_name"],
                "platform": course["platform"],
                "skills": matched_skills,
                "level": course["level"],
                "duration": course["duration"],
                "url": course["url"],
                "relevance": len(matched_skills)
            })

    recommendations.sort(
        key=lambda x: x["relevance"],
        reverse=True
    )

    return recommendations[:top_k]


if __name__ == "__main__":

    missing_skills = [
        "Django",
        "REST APIs"
    ]

    results = recommend_courses(
        missing_skills
    )

    for course in results:
        print("\nCourse:", course["course_name"])
        print("Platform:", course["platform"])
        print("Skills:", course["skills"])
        print("Level:", course["level"])
        print("Duration:", course["duration"])
        print("URL:", course["url"])# Course recommendation agent
