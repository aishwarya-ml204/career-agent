
from agents.profile_parser import parse_profile
from agents.job_matcher import match_jobs
from agents.gap_analyzer import analyze_gap
from agents.course_recommender import recommend_courses

def run_career_analysis(profile_text, top_k=5):

    # Step 1: Parse user profile
    profile = parse_profile(profile_text)
    user_skills = profile["skills"]
    print("Detected location:", profile.get("location"))
    # Step 2: Find matching jobs
    jobs = match_jobs(
    user_skills,
    location=profile.get("location"),
    top_k=top_k
)

    results = []

    # Step 3: Analyze skill gaps for each job
    for _, job in jobs.iterrows():

        gap = analyze_gap(
            user_skills,
            job["REQUIRED_SKILLS"]
        )
        courses = recommend_courses(
    gap["missing_skills"],
    top_k=3
        )
        


        results.append({
            "job_id": job["JOB_ID"],
            "job_title": job["JOB_TITLE"],
            "company": job["COMPANY"],
            "location": job["LOCATION"],
            "match_score": round(float(job["match_score"]), 3),
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
            "gap_percentage": gap["gap_percentage"],
            "recommended_courses": courses
        })

    return {
        "profile": profile,
        "jobs": results
    }


if __name__ == "__main__":

    profile_text = """
I am a B.Tech Computer Science student.
I live in Bengaluru, Karnataka.
I know Python, SQL, Pandas and NumPy.
I am interested in machine learning and data science.
"""

    result = run_career_analysis(profile_text)

    print("\nUSER SKILLS")
    print("-----------")
    print(result["profile"]["skills"])

    print("\nJOB RECOMMENDATIONS")
    print("-------------------")

    for job in result["jobs"]:

        print("\nJob:", job["job_title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Match Score:", job["match_score"])
        print("Missing Skills:", job["missing_skills"])
        print("Gap:", job["gap_percentage"], "%")

        print("Recommended Courses:")

        for course in job["recommended_courses"]:
            print(
            "  -",
            course["course_name"],
            "|",
            course["platform"]
            )