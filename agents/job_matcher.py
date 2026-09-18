# Job matching agent
import pandas as pd
from sentence_transformers import SentenceTransformer, util


MODEL_NAME = "all-MiniLM-L6-v2"


def load_jobs():
    return pd.read_csv("data/job.csv")

def match_jobs(user_skills, location=None, top_k=5):
    jobs = load_jobs()

    # Filter jobs by location if provided
    if location:
        location = location.lower().strip()

        # Handle common city name variation
        location_aliases = {
            "bangalore": "bengaluru",
            "bombay": "mumbai",
            "gurgaon": "gurugram"
        }

        location = location_aliases.get(location, location)

        jobs = jobs[
            jobs["LOCATION"]
            .fillna("")
            .str.lower()
            .str.contains(location, na=False)
        ]

    # If no jobs are available in that location
    if jobs.empty:
        return jobs

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

    jobs = jobs.copy()
    jobs["match_score"] = similarities.cpu().numpy()

    return jobs.sort_values(
        "match_score",
        ascending=False
    ).head(top_k)



if __name__ == "__main__":

    user_skills = [
        "python",
        "sql",
        "pandas",
        "numpy"
    ]

    results = match_jobs(user_skills)

    print(
        results[
            [
                "JOB_ID",
                "JOB_TITLE",
                "COMPANY",
                "LOCATION",
                "REQUIRED_SKILLS",
                "match_score"
            ]
        ].to_string(index=False)
    )