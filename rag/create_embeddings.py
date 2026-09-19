# Create embeddings for jobs and courses

import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb


# ==============================
# LOAD DATASETS
# ==============================

jobs = pd.read_csv("data/job.csv")
courses = pd.read_csv("data/courses.csv")


# ==============================
# LOAD EMBEDDING MODEL
# ==============================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ==============================
# CREATE CHROMADB CLIENT
# ==============================

client = chromadb.PersistentClient(
    path="chroma_db"
)


# ==============================
# CREATE COLLECTIONS
# ==============================

job_collection = client.get_or_create_collection(
    name="jobs"
)

course_collection = client.get_or_create_collection(
    name="courses"
)


# ==============================
# JOB EMBEDDINGS
# ==============================

job_documents = (
    jobs["JOB_TITLE"].fillna("") + " " +
    jobs["REQUIRED_SKILLS"].fillna("") + " " +
    jobs["JOB_DESCRIPTION"].fillna("")
).tolist()


job_embeddings = model.encode(
    job_documents
).tolist()


job_collection.add(
    ids=jobs["JOB_ID"].astype(str).tolist(),

    documents=job_documents,

    embeddings=job_embeddings,

    metadatas=jobs[
        [
            "JOB_TITLE",
            "COMPANY",
            "LOCATION",
            "EXPERIENCE",
            "REQUIRED_SKILLS",
            "SOURCE_URL"
        ]
    ].fillna("").to_dict("records")
)


# ==============================
# COURSE EMBEDDINGS
# ==============================

# Include the new course information
# in the text used for embeddings.

course_documents = (
    courses["course_name"].fillna("") + " " +
    courses["skills"].fillna("") + " " +
    courses["level"].fillna("") + " " +
    courses["duration"].fillna("") + " " +
    courses["duration_hours"].fillna("").astype(str) + " " +
    courses["cost"].fillna("")
).tolist()


course_embeddings = model.encode(
    course_documents
).tolist()


# Store all course information as metadata

course_collection.add(
    ids=courses["course_id"].astype(str).tolist(),

    documents=course_documents,

    embeddings=course_embeddings,

    metadatas=courses[
        [
            "course_name",
            "platform",
            "skills",
            "level",
            "duration",
            "duration_hours",
            "cost",
            "url"
        ]
    ].fillna("").to_dict("records")
)


# ==============================
# SUCCESS MESSAGE
# ==============================

print("RAG database created successfully!")

print(
    "Jobs stored:",
    len(jobs)
)

print(
    "Courses stored:",
    len(courses)
)

print(
    "Course metadata fields:",
    [
        "course_name",
        "platform",
        "skills",
        "level",
        "duration",
        "duration_hours",
        "cost",
        "url"
    ]
)