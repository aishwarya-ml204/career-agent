from retriever import find_matching_courses


def recommend_courses(missing_skills, n_results=5):
    """Find courses for the missing skills."""

    if not missing_skills:
        return []

    # Convert list of missing skills into a search query
    query = ", ".join(missing_skills)

    results = find_matching_courses(
        query,
        n_results=n_results
    )

    return results["metadatas"][0]


if __name__ == "__main__":

    missing_skills = [
        "TensorFlow",
        "Docker"
    ]

    courses = recommend_courses(missing_skills)

    print("\n========== RECOMMENDED COURSES ==========")

    for i, course in enumerate(courses):

        print(f"\nCourse {i + 1}: {course['course_name']}")
        print(f"Platform: {course['platform']}")
        print(f"Skills: {course['skills']}")
        print(f"Level: {course['level']}")
        print(f"Duration: {course['duration']}")
        print(f"URL: {course['url']}")