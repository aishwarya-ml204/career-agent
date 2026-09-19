import pandas as pd
import re

COURSES_FILE = "data/courses.csv"


def normalize_skill(skill):
    skill = str(skill).lower().strip()

    replacements = {
        "ml": "machine learning",
        "machine-learning": "machine learning",
        "powerbi": "power bi",
        "nodejs": "node.js",
        "js": "javascript",
        "py": "python",
        "scikit learn": "scikit-learn",
        "data visualisation": "data visualization",
        "pytorch or tensorflow": "deep learning",
        "basic deep learning": "deep learning",
        "vector databases": "vector database",
    }

    return replacements.get(skill, skill)


def split_skills(skill_text):
    if not skill_text:
        return []

    skills = re.split(r"[,;|/\n]+", str(skill_text))

    return [
        normalize_skill(skill)
        for skill in skills
        if skill.strip()
    ]


def skill_matches(missing_skill, course_skill):
    missing_skill = normalize_skill(missing_skill)
    course_skill = normalize_skill(course_skill)

    if missing_skill == course_skill:
        return True

    related_skills = {
        "scikit-learn": [
            "scikit-learn"
        ],

        "statistics": [
            "statistics",
            "descriptive statistics"
        ],

        "deep learning": [
            "deep learning"
        ],

        "data visualization": [
            "data visualization"
        ],

        "docker": [
            "docker",
            "docker basics",
            "containers"
        ],

        "kubernetes": [
            "kubernetes"
        ],

        "spark": [
            "spark"
        ],

        "airflow": [
            "airflow"
        ],

        "etl": [
            "etl",
            "etl basics",
            "etl concepts"
        ],

        "data modeling": [
            "data modeling"
        ],

        "kafka": [
            "kafka",
            "streaming"
        ],

        "llms": [
            "llms"
        ],

        "transformers": [
            "transformers"
        ],

        "prompt engineering": [
            "prompt engineering"
        ],

        "rag": [
            "rag"
        ],

        "vector database": [
            "vector database",
            "vector databases (pinecone/faiss)"
        ],

        "apis": [
            "apis",
            "rest apis",
            "api gateway"
        ],

        "pytorch": [
            "pytorch",
            "pytorch or tensorflow"
        ],
    }

    return course_skill in related_skills.get(
        missing_skill,
        []
    )


def recommend_courses(missing_skills, top_k=5):
    df = pd.read_csv(COURSES_FILE)

    recommendations = []

    for _, row in df.iterrows():

        course_skills = split_skills(row["skills"])

        matched_skills = []

        for missing_skill in missing_skills:

            for course_skill in course_skills:

                if skill_matches(missing_skill, course_skill):
                    matched_skills.append(missing_skill)
                    break

        if matched_skills:

            recommendations.append({
                "course_id": row["course_id"],
                "course_name": row["course_name"],
                "platform": row["platform"],
                "skills": course_skills,
                "level": row["level"],

                # Existing course information
                "duration": row["duration"],

                # New compulsory add-on information
                "duration_hours": row["duration_hours"],
                "cost": row["cost"],

                "url": row["url"],

                "matched_skills": list(
                    set(matched_skills)
                ),

                "exact_matches": len(
                    set(matched_skills)
                ),
            })

    recommendations.sort(
        key=lambda x: x["exact_matches"],
        reverse=True
    )

    return recommendations[:top_k]


if __name__ == "__main__":

    test_missing_skills = [
        "scikit-learn",
        "statistics",
        "deep learning"
    ]

    courses = recommend_courses(
        test_missing_skills,
        top_k=5
    )

    print("\n==============================")
    print("COURSE RECOMMENDATIONS")
    print("==============================")

    for course in courses:

        print("\nCourse:", course["course_name"])
        print("Platform:", course["platform"])
        print("Level:", course["level"])
        print("Duration:", course["duration"])
        print("Duration Hours:", course["duration_hours"])
        print("Cost:", course["cost"])
        print("Matched Skills:", course["matched_skills"])
        print("URL:", course["url"])