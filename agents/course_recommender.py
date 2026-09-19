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

        # Handle variations
        "scikit learn": "scikit-learn",
        "scikit learn ": "scikit-learn",
        "data visualisation": "data visualization",
        "pytorch or tensorflow": "deep learning",
        "basic deep learning": "deep learning",
        "aws (s3, glue, redshift)": "aws",
        "vector databases": "vector database",
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


def skill_matches(missing_skill, course_skill):
    """
    Check whether a course skill is relevant to a missing skill.
    """

    missing_skill = normalize_skill(missing_skill)
    course_skill = normalize_skill(course_skill)

    # Exact match
    if missing_skill == course_skill:
        return True

    # Useful related mappings
    related_skills = {
        "scikit-learn": ["scikit-learn"],
        "statistics": ["statistics", "descriptive statistics"],
        "basic deep learning": ["deep learning", "basic deep learning"],
        "deep learning": ["deep learning", "basic deep learning"],
        "data visualization": ["data visualization"],
        "docker": ["docker", "docker basics", "containers"],
        "kubernetes": ["kubernetes"],
        "spark": ["spark"],
        "airflow": ["airflow"],
        "etl": ["etl", "etl basics", "etl concepts"],
        "data modeling": ["data modeling"],
        "kafka": ["kafka", "streaming"],
        "llms": ["llms"],
        "transformers": ["transformers"],
        "prompt engineering": ["prompt engineering"],
        "rag": ["rag"],
        "vector database": [
            "vector database",
            "vector databases (pinecone/faiss)"
        ],
        "apis": ["apis", "rest apis", "api gateway"],
        "pytorch": ["pytorch", "pytorch or tensorflow"],
    }

    if missing_skill in related_skills:
        return course_skill in related_skills[missing_skill]

    return False


def recommend_courses(missing_skills, top_k=5):
    """
    Recommend courses based on the candidate's missing skills.
    """

    if not missing_skills:
        return []

    courses = pd.read_csv(COURSES_FILE)

    recommendations = []

    for _, course in courses.iterrows():

        course_skills = split_skills(course["skills"])

        matched_skills = []

        for missing_skill in missing_skills:

            for course_skill in course_skills:

                if skill_matches(missing_skill, course_skill):

                    matched_skills.append(
                        normalize_skill(missing_skill)
                    )

                    break

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

    # Remove duplicate skills inside a course
    for course in recommendations:
        course["skills"] = list(
            dict.fromkeys(course["skills"])
        )

    # Highest number of matched missing skills first
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
        print("URL:", course["url"])