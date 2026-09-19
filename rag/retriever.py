import chromadb
from sentence_transformers import SentenceTransformer


# ==============================
# LOAD EMBEDDING MODEL
# ==============================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ==============================
# CONNECT TO CHROMADB
# ==============================

client = chromadb.PersistentClient(
    path="chroma_db"
)


# ==============================
# GET COLLECTIONS
# ==============================

job_collection = client.get_collection(
    name="jobs"
)

course_collection = client.get_collection(
    name="courses"
)


# ==============================
# MATCHING JOBS
# ==============================

def find_matching_jobs(
    user_skills,
    n_results=5
):
    """
    Find jobs related to the user's skills.
    """

    query_embedding = model.encode(
        user_skills
    ).tolist()

    results = job_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results


# ==============================
# MATCHING COURSES
# ==============================

def find_matching_courses(
    missing_skills,
    n_results=5
):
    """
    Find courses related to missing skills.

    Returns course information including:
    - course name
    - platform
    - skills
    - level
    - duration
    - duration hours
    - cost
    - URL
    """

    query_embedding = model.encode(
        missing_skills
    ).tolist()

    results = course_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results


# ==============================
# TEST
# ==============================

if __name__ == "__main__":

    skills = "Python machine learning SQL"

    print("\n--- MATCHING JOBS ---")

    jobs = find_matching_jobs(
        skills
    )

    for job in jobs["metadatas"][0]:

        print(
            job["JOB_TITLE"],
            "|",
            job["COMPANY"],
            "|",
            job["LOCATION"]
        )

    print("\n--- RECOMMENDED COURSES ---")

    courses = find_matching_courses(
        "machine learning Python"
    )

    for course in courses["metadatas"][0]:

        print(
            "\nCourse:",
            course["course_name"]
        )

        print(
            "Platform:",
            course["platform"]
        )

        print(
            "Level:",
            course["level"]
        )

        print(
            "Duration:",
            course["duration"]
        )

        print(
            "Duration Hours:",
            course["duration_hours"]
        )

        print(
            "Cost:",
            course["cost"]
        )

        print(
            "URL:",
            course["url"]
        )