from retriever import find_matching_jobs
from skill_gap import find_skill_gap


# Example user profile
user_skills = "Python, SQL, Machine Learning"


# Retrieve relevant jobs
jobs = find_matching_jobs(user_skills, n_results=5)


print("\n========== JOB MATCHING + SKILL GAP ==========")


for i, job in enumerate(jobs["metadatas"][0]):

    print(f"\nJob {i + 1}: {job['JOB_TITLE']}")
    print(f"Company: {job['COMPANY']}")
    print(f"Location: {job['LOCATION']}")

    # Find missing skills
    gap = find_skill_gap(
        user_skills,
        job["REQUIRED_SKILLS"]
    )

    print("Matched Skills:", ", ".join(gap["matched_skills"]))

    print("Missing Skills:", ", ".join(gap["missing_skills"]))