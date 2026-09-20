# 🧭 Career Compass

### AI-Based Career Guidance and Skill Gap Analysis Agent

Career Compass is an AI-powered career guidance system that connects a user's current skills with real job opportunities and identifies the skills they need to develop for those jobs.

Instead of giving generic course recommendations, the system analyzes curated job postings, identifies skill gaps, and recommends targeted training courses based on the opportunities available.

---

## 🎯 Problem Statement

Job seekers often do not know which skills are missing for the jobs available in their preferred location.

Generic career advice may recommend courses without considering actual job requirements.

Career Compass solves this problem by:

- Understanding the candidate's profile and skills
- Matching the candidate with relevant job postings
- Identifying specific missing skills
- Ranking skill gaps based on job opportunities
- Recommending courses to close those gaps
- Estimating the time required to become job-ready

---

## 🚀 Key Features

### 1. Profile Intake
Accepts candidate information through:

- Resume upload
- Preferred job location
- Career interests

The system extracts relevant information such as skills, education, experience and projects.

### 2. Job Matching
Matches the candidate's skills against curated job postings using semantic similarity.

### 3. Skill Gap Analysis
For each matched job, the system identifies:

- Matched skills
- Missing skills
- Skill gap percentage

### 4. Opportunity-Based Skill Ranking
Missing skills are ranked according to how many relevant job opportunities require them.

This helps the candidate focus on skills that can potentially unlock more opportunities.

### 5. Course Recommendation
The system maps missing skills to relevant courses from curated course data.

Course information includes:

- Course name
- Platform
- Skills
- Level
- Duration
- Learning hours
- Cost
- Course URL

### 6. Time-to-Ready Estimate
The system estimates how much learning time is required to complete the recommended training path.

Estimated time is calculated using:

Total Learning Hours ÷ Weekly Study Hours × 7

The system also supports a free-course-only filter.

### 7. AI Career Reasoning
Gemini-based reasoning provides:

- Career summary
- Explanation of why priority skills matter
- Job-specific insights
- Personalized learning strategy

### 8. RAG-Based Retrieval
ChromaDB and Sentence Transformers are used to retrieve relevant jobs and courses from the curated knowledge base.

### 9. LangGraph Workflow
The career analysis is organized as an agent workflow:

Profile Parsing
        ↓
Job Matching
        ↓
Skill Gap Analysis
        ↓
Opportunity Ranking
        ↓
Course Recommendation
        ↓
Training Path
        ↓
Time-to-Ready

---

## 🛠️ Technology Stack

### Frontend
- Streamlit

### Programming Language
- Python

### AI / Machine Learning
- Sentence Transformers
- Gemini LLM

### RAG
- ChromaDB
- Sentence Transformers

### Agent Orchestration
- LangGraph

### Data Processing
- Pandas

### Resume Processing
- PyPDF
- python-docx

---

## 📂 Project Structure

```text
career-agent/
│
├── app/
│   ├── app.py
│   ├── pages/
│   │   ├── home.py
│   │   ├── profile.py
│   │   ├── analysis.py
│   │   ├── jobs.py
│   │   ├── job_details.py
│   │   ├── skill_gaps.py
│   │   └── learning_path.py
│   │
│   └── assets/
│
├── agents/
│   ├── profile_parser.py
│   ├── job_matcher.py
│   ├── gap_analyzer.py
│   ├── opportunity_ranker.py
│   ├── course_recommender.py
│   ├── training_path.py
│   └── career_pipeline.py
│
├── rag/
│   ├── create_embeddings.py
│   └── retriever.py
│
├── workflow/
│   └── graph.py
│
├── data/
│   ├── job.csv
│   └── courses.csv
│
├── requirements.txt
└── README.md
