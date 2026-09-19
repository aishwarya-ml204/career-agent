from retriever import find_matching_courses


def recommend_courses(missing_skills, n_results=5):
    if not missing_skills:
        return []

    recommendations = []

    for skill in missing_skills:
        results = find_matching_courses(skill, n_results=3)

        for course in results["metadatas"][0]:
            course_skills = course["skills"].lower()

            # Check whether the course directly covers the missing skill
            if skill.lower() in course_skills:
                recommendations.append({
                    "missing_skill": skill,
                    "course_name": course["course_name"],
                    "platform": course["platform"],
                    "skills": course["skills"],
                    "level": course["level"],
                    "duration": course["duration"],
                    "url": course["url"]
                })

    return recommendations


if __name__ == "__main__":

    missing_skills = [
        "basic deep learning",
        "git",
        "pandas",
        "scikit-learn",
        "statistics"
    ]

    courses = recommend_courses(missing_skills)

    print("\n========== RECOMMENDED COURSES ==========")

    if not courses:
        print("No exact course matches found.")

    for i, course in enumerate(courses):
        print(f"\nCourse {i + 1}")
        print("Missing Skill:", course["missing_skill"])
        print("Course:", course["course_name"])
        print("Platform:", course["platform"])
        print("Skills:", course["skills"])
        print("Level:", course["level"])
        print("Duration:", course["duration"])
        print("URL:", course["url"])