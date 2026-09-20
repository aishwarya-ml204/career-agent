from agents.course_recommender import recommend_courses


def build_training_path(priority_skills, max_steps=5):

    training_path = []

    for item in priority_skills:

        skill = str(item["skill"]).strip(" []'\"")
        job_count = item["job_count"]

        courses = recommend_courses(
            [skill],
            10
        )

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

            if all(
                word in course_name
                for word in skill_words
            ):
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

            # Course duration
            "duration": selected_course["duration"],

            # Course duration in hours
            "duration_hours": selected_course["duration_hours"],

            # Course cost
            "cost": selected_course["cost"],

            "url": selected_course["url"],

            # Number of jobs this skill could potentially unlock
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

    training_path = build_training_path(
        priority_skills
    )

    print("\n====================")
    print("TRAINING PATH")
    print("====================")

    for item in training_path:

        print(
            f"\nStep {item['step']}: "
            f"{item['skill']}"
        )

        print(
            f"Course: "
            f"{item['course_name']}"
        )

        print(
            f"Platform: "
            f"{item['platform']}"
        )

        print(
            f"Level: "
            f"{item['level']}"
        )

        print(
            f"Duration: "
            f"{item['duration']}"
        )

        print(
            f"Duration Hours: "
            f"{item['duration_hours']}"
        )

        print(
            f"Cost: "
            f"{item['cost']}"
        )

        print(
            f"Jobs potentially unlocked: "
            f"{item['jobs_unlocked']}"
        )