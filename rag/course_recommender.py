from rag.retriever import find_matching_courses


def normalize(text):
    return text.lower().strip()


def recommend_courses(missing_skills, n_results=3):

    if not missing_skills:
        return []

    recommendations = []
    seen_courses = set()

    for skill in missing_skills:

        skill = normalize(skill)

        results = find_matching_courses(skill, n_results=5)

        for course in results["metadatas"][0]:

            course_name = course["course_name"]

            if course_name in seen_courses:
                continue

            course_skills = normalize(course["skills"])

            # Match the complete skill phrase
            if skill in course_skills:

                recommendations.append({
                    "missing_skill": skill,
                    "course_name": course_name,
                    "platform": course["platform"],
                    "skills": course["skills"],
                    "level": course["level"],
                    "duration": course["duration"],
                    "url": course["url"]
                })

                seen_courses.add(course_name)

                # Maximum 3 courses for each missing skill
                skill_count = sum(
                    1 for c in recommendations
                    if c["missing_skill"] == skill
                )

                if skill_count >= n_results:
                    break

    return recommendations