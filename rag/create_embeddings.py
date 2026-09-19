# Create embeddings for jobs and courses
import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

# Load datasets
jobs = pd.read_csv("data/job.csv")
courses = pd.read_csv("data/courses.csv")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create collections
job_collection = client.get_or_create_collection(name="jobs")
course_collection = client.get_or_create_collection(name="courses")

# ---------------- JOB EMBEDDINGS ----------------

job_documents = (
    jobs["JOB_TITLE"].fillna("") + " " +
    jobs["REQUIRED_SKILLS"].fillna("") + " " +
    jobs["JOB_DESCRIPTION"].fillna("")
).tolist()

job_embeddings = model.encode(job_documents).tolist()

job_collection.add(
    ids=jobs["JOB_ID"].astype(str).tolist(),
    documents=job_documents,
    embeddings=job_embeddings,
    metadatas=jobs[
        ["JOB_TITLE", "COMPANY", "LOCATION", "EXPERIENCE", "REQUIRED_SKILLS", "SOURCE_URL"]
    ].fillna("").to_dict("records")
)

# ---------------- COURSE EMBEDDINGS ----------------

course_documents = (
    courses["course_name"].fillna("") + " " +
    courses["skills"].fillna("") + " " +
    courses["level"].fillna("")
).tolist()

course_embeddings = model.encode(course_documents).tolist()

course_collection.add(
    ids=courses["course_id"].astype(str).tolist(),
    documents=course_documents,
    embeddings=course_embeddings,
    metadatas=courses[
        ["course_name", "platform", "skills", "level", "duration", "url"]
    ].fillna("").to_dict("records")
)

print("RAG database created successfully!")
print("Jobs stored:", len(jobs))
print("Courses stored:", len(courses))