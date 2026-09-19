from agents.course_recommender import recommend_courses


def build_training_path(priority_skills, max_steps=5):

    training_path = []

    for item in priority_skills:

        skill = item["skill"]
        job_count = item["job_count"]

        courses = recommend_courses([skill], top_k=10)

        if not courses:
            continue

        # Rank courses by how directly their name matches the skill
        skill_lower = skill.lower().strip()

        def course_priority(course):
            course_name = course["course_name"].lower().strip()

            # Exact phrase in course name
            if skill_lower in course_name:
                return 3

            # Individual words from the skill in course name
            skill_words = skill_lower.split()
            if all(word in course_name for word in skill_words):
                return 2

            return 1

        courses.sort(
            key=course_priority,
            reverse=True
        )

        selected_course = courses[0]

        training_path.append({
            "step": len(training_path) + 1,
            "skill": skill,
            "course_name": selected_course["course_name"],
            "platform": selected_course["platform"],
            "level": selected_course["level"],
            "duration": selected_course["duration"],
            "url": selected_course["url"],
            "jobs_unlocked": job_count
        })

        if len(training_path) >= max_steps:
            break

    return training_path


if __name__ == "__main__":

    priority_skills = [
        {"skill": "scikit-learn", "job_count": 3},
        {"skill": "statistics", "job_count": 3},
        {"skill": "deep learning", "job_count": 2},
        {"skill": "git", "job_count": 1}
    ]

    training_path = build_training_path(priority_skills)

    print("\n====================")
    print("TRAINING PATH")
    print("====================")

    for item in training_path:
        print(f"\nStep {item['step']}: {item['skill']}")
        print(f"Course: {item['course_name']}")
        print(f"Platform: {item['platform']}")
        print(f"Level: {item['level']}")
        print(f"Jobs potentially unlocked: {item['jobs_unlocked']}")