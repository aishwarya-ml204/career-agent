import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util


# ============================================================
# MODEL
# ============================================================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# DATASET
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

JOBS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "job.csv"
)

jobs_df = pd.read_csv(JOBS_FILE)


# ============================================================
# LOCATION NORMALIZATION
# ============================================================

def normalize_location(location):

    if location is None:
        return ""

    location = str(location).lower().strip()

    # Remove extra spaces
    location = " ".join(
        location.split()
    )

    replacements = {
        "banglore": "bengaluru",
        "bangalore": "bengaluru",
        "blr": "bengaluru",

        "mysore": "mysuru",

        "bombay": "mumbai",

        "madras": "chennai",

        "calcutta": "kolkata",

        "new delhi": "delhi"
    }

    for old, new in replacements.items():

        if location == old:

            location = new

            break

        if location.startswith(old + ","):

            location = new + location[len(old):]

            break

        if location.startswith(old + " "):

            location = new + location[len(old):]

            break

    return location


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):

    if pd.isna(text):
        return ""

    return str(text).lower().strip()


# ============================================================
# LOCATION MATCH
# ============================================================

def location_matches(
    user_location,
    job_location
):

    user = normalize_location(
        user_location
    )

    job = normalize_location(
        job_location
    )

    if not user:
        return True

    if not job:
        return False

    # Exact normalized match
    if user == job:
        return True

    # City contained in "City, State"
    user_city = user.split(",")[0].strip()
    job_city = job.split(",")[0].strip()

    if user_city == job_city:
        return True

    return False


# ============================================================
# JOB MATCHING
# ============================================================

def match_jobs(
    user_skills,
    location=None,
    top_k=5
):

    # --------------------------------------------------------
    # Normalize user skills
    # --------------------------------------------------------

    if isinstance(user_skills, list):

        skills_text = ", ".join(
            str(skill)
            for skill in user_skills
        )

    else:

        skills_text = str(
            user_skills or ""
        )


    skills_text = normalize_text(
        skills_text
    )


    # --------------------------------------------------------
    # No skills
    # --------------------------------------------------------

    if not skills_text:

        return []


    # --------------------------------------------------------
    # LOCATION FILTER FIRST
    # --------------------------------------------------------

    filtered_df = jobs_df.copy()


    if location:

        matching_indexes = []

        for index, row in filtered_df.iterrows():

            job_location = row.get(
                "LOCATION",
                ""
            )

            if location_matches(
                location,
                job_location
            ):

                matching_indexes.append(
                    index
                )


        # ----------------------------------------------------
        # IMPORTANT:
        # If the requested location has no jobs,
        # return EMPTY.
        #
        # Never show jobs from another city.
        # ----------------------------------------------------

        if not matching_indexes:

            print(
                f"No jobs found for location: {location}"
            )

            return []


        filtered_df = filtered_df.loc[
            matching_indexes
        ].copy()


    # --------------------------------------------------------
    # CREATE JOB TEXT
    # --------------------------------------------------------

    job_texts = []

    for _, row in filtered_df.iterrows():

        text = f"""
        {row.get('JOB_TITLE', '')}
        {row.get('REQUIRED_SKILLS', '')}
        {row.get('JOB_DESCRIPTION', '')}
        """

        job_texts.append(
            normalize_text(text)
        )


    # --------------------------------------------------------
    # CREATE EMBEDDINGS
    # --------------------------------------------------------

    user_embedding = model.encode(
        skills_text,
        convert_to_tensor=True
    )

    job_embeddings = model.encode(
        job_texts,
        convert_to_tensor=True
    )


    # --------------------------------------------------------
    # SIMILARITY
    # --------------------------------------------------------

    similarities = util.cos_sim(
        user_embedding,
        job_embeddings
    )[0]


    # --------------------------------------------------------
    # ADD MATCH SCORE
    # --------------------------------------------------------

    filtered_df["match_score"] = [
        float(score) * 100
        for score in similarities
    ]


    # --------------------------------------------------------
    # SORT
    # --------------------------------------------------------

    filtered_df = filtered_df.sort_values(
        by="match_score",
        ascending=False
    )


    # --------------------------------------------------------
    # BUILD RESULTS
    # --------------------------------------------------------

    results = []


    for _, row in filtered_df.head(
        top_k
    ).iterrows():

        results.append(
            {
                "job_id": row.get(
                    "JOB_ID",
                    ""
                ),

                "job_title": row.get(
                    "JOB_TITLE",
                    ""
                ),

                "company": row.get(
                    "COMPANY",
                    ""
                ),

                "location": row.get(
                    "LOCATION",
                    ""
                ),

                "match_score": round(
                    float(
                        row.get(
                            "match_score",
                            0
                        )
                    ),
                    1
                ),

                "required_skills": row.get(
                    "REQUIRED_SKILLS",
                    ""
                ),

                "job_description": row.get(
                    "JOB_DESCRIPTION",
                    ""
                ),

                "source_url": row.get(
                    "SOURCE_URL",
                    ""
                )
            }
        )


    return results