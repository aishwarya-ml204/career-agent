import pandas as pd
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"


def load_jobs():
    return pd.read_csv("data/job.csv")


def normalize_city(location):
    if not location:
        return ""

    location = str(location).lower().strip()

    # Only use the city part
    city = location.split(",")[0].strip()

    aliases = {
        "bangalore": "bengaluru",
        "bengaluru": "bengaluru",
        "bombay": "mumbai",
        "mumbai": "mumbai",
        "gurgaon": "gurugram",
        "gurugram": "gurugram",
    }

    return aliases.get(city, city)


def match_jobs(user_skills, location=None, top_k=5):

    jobs = load_jobs()

    print("\n--- JOB MATCHING ---")
    print("Total jobs:", len(jobs))
    print("User location:", location)

    # ------------------------------------------
    # Location filtering
    # ------------------------------------------

    if location:

        user_city = normalize_city(location)

        print("Normalized user city:", user_city)

        jobs["normalized_city"] = (
            jobs["LOCATION"]
            .fillna("")
            .apply(normalize_city)
        )

        jobs = jobs[
            jobs["normalized_city"] == user_city
        ].copy()

        print(
            "Jobs after location filter:",
            len(jobs)
        )

    if jobs.empty:

        print("No jobs found for location:", location)

        return jobs

    # ------------------------------------------
    # Semantic skill matching
    # ------------------------------------------

    model = SentenceTransformer(MODEL_NAME)

    user_text = ", ".join(user_skills)

    user_embedding = model.encode(
        user_text,
        convert_to_tensor=True
    )

    job_texts = (
        jobs["REQUIRED_SKILLS"]
        .fillna("")
        .astype(str)
        .tolist()
    )

    job_embeddings = model.encode(
        job_texts,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        user_embedding,
        job_embeddings
    )[0]

    jobs["match_score"] = similarities.cpu().numpy()

    jobs = jobs.sort_values(
        "match_score",
        ascending=False
    )

    # Remove temporary column
    if "normalized_city" in jobs.columns:
        jobs = jobs.drop(
            columns=["normalized_city"]
        )

    return jobs.head(top_k)