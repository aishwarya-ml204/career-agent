import streamlit as st
import io
from pypdf import PdfReader
from docx import Document
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from workflow.graph import build_graph

def extract_text_from_resume(uploaded_file):
    """
    Extract text from an uploaded PDF or DOCX resume.
    """

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".pdf"):
            pdf_reader = PdfReader(uploaded_file)

            text = []
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""
                text.append(page_text)

            return "\n".join(text).strip()

        elif file_name.endswith(".docx"):
            document = Document(uploaded_file)

            text = []
            for paragraph in document.paragraphs:
                text.append(paragraph.text)

            return "\n".join(text).strip()

        else:
            raise ValueError(
                "Unsupported file format. Please upload a PDF or DOCX file."
            )

    except Exception as error:
        raise RuntimeError(
            f"Could not extract text from the resume: {error}"
        ) from error

st.set_page_config(
    page_title="Career Compass",
    page_icon="ðŸ§­",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background: #F7F9FC;
}

[data-testid="stSidebar"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 0.5rem;
    padding-bottom: 3rem;
}
</style>
""", unsafe_allow_html=True)



# ============================================================
# PAGES
# ============================================================

home = st.Page(
    "pages/home.py",
    title="Dashboard",
    icon=":material/home:"
)

profile = st.Page(
    "pages/profile.py",
    title="Profile",
    icon=":material/person:"
)

analysis = st.Page(
    "pages/analysis.py",
    title="AI Analysis",
    icon=":material/psychology:"
)

jobs = st.Page(
    "pages/jobs.py",
    title="Jobs",
    icon=":material/work:"
)

job_details = st.Page(
    "pages/job_details.py",
    title="Job Details",
    icon=":material/description:"
)

skill_gaps = st.Page(
    "pages/skill_gaps.py",
    title="Skill Gaps",
    icon=":material/target:"
)

learning = st.Page(
    "pages/learning_path.py",
    title="Learning Path",
    icon=":material/school:"
)

# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    [
        home,
        profile,
        analysis,
        jobs,
        job_details,
        skill_gaps,
        learning
    ],
    position="hidden"
)
pg.run()
st.divider()


# --------------------------------------------------
# Candidate Profile
# --------------------------------------------------

st.header("ðŸ‘¤ Candidate Profile")

resume_file = st.file_uploader(
    "ðŸ“„ Upload Your Resume",
    type=["pdf", "docx"],
    help="Upload your resume in PDF or DOCX format."
)

st.caption(
    "Your resume will be used to automatically extract "
    "education, skills, experience and projects."
)

col1, col2 = st.columns(2)

with col1:
    location = st.text_input(
        "ðŸ“ Preferred Job Location",
        placeholder="Example: Bengaluru, Karnataka"
    )

with col2:
    interests = st.text_input(
        "â¤ï¸ Career Interests",
        placeholder="Example: Machine Learning, Data Science"
    )


# --------------------------------------------------
# Training Preferences
# --------------------------------------------------

st.header("âš™ï¸ Training Preferences")

pref_col1, pref_col2 = st.columns(2)

with pref_col1:
    free_only = st.checkbox(
        "ðŸ†“ Show only free courses"
    )

with pref_col2:
    weekly_hours = st.number_input(
        "â° Study hours per week",
        min_value=1,
        max_value=60,
        value=10,
        step=1
    )

st.caption(
    "Time-to-ready is an estimate based on the total course hours "
    "and your selected weekly study time."
)

st.write("")


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

analyze_button = st.button(
    "ðŸš€ Analyze My Career",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Career Analysis
# --------------------------------------------------

if analyze_button:

    if resume_file is None:
        st.warning(
            "ðŸ“„ Please upload your resume first."
        )

    else:

        try:

            # ------------------------------------------
            # Extract resume text
            # ------------------------------------------

            with st.spinner("ðŸ“„ Reading your resume..."):

                resume_text = extract_text_from_resume(
                    resume_file
                )

            if not resume_text or not resume_text.strip():

                st.error(
                    "âŒ Could not extract text from this resume. "
                    "Please try another PDF or DOCX file."
                )

                st.stop()


            # ------------------------------------------
            # Build profile text
            # ------------------------------------------

            profile_text = f"""
Resume Information:

{resume_text}

Additional Candidate Information:

Preferred Job Location:
{location}

Career Interests:
{interests}
"""


            # ------------------------------------------
            # Run Career Agent
            # ------------------------------------------
            with st.spinner(
                "ðŸ”„ Analyzing your resume and finding opportunities..."
            ):
                career_graph = build_graph()

                result = career_graph.invoke(
                    {
                        "profile_text": profile_text,
                        "profile": {},
                        "jobs": [],
                        "priority_skills": [],
                        "training_path": []
                    }
                )

                st.write(
                    "DEBUG - Result keys:",
                    list(result.keys())
                )

                st.write(
                    "DEBUG - Training path:",
                    result.get("training_path")
                )

                st.write(
                    "DEBUG - Training summary:",
                    result.get("training_summary")
                )

                training_path = result.get("training_path", [])
                st.subheader("ðŸ›£ï¸ Personalized Training Path")

                if training_path:
                    for index, step in enumerate(training_path, start=1):
                        st.markdown(f"### Step {index}")

                        if isinstance(step, dict):
                            st.write(
                                step.get(
                                    "course_name",
                                    step.get("title", "Training course")
                                )
                            )
                            st.write(step.get("description", ""))
                            st.write(
                                f"Duration: {step.get('duration', 'N/A')}"
                            )
                            st.write(
                                f"Cost: {step.get('cost', 'N/A')}"
                            )
                        else:
                            st.write(step)
                else:
                    st.info("No training path could be generated.")

                st.success(
                    "Career analysis completed successfully! ðŸŽ‰"
                )

            # --------------------------------------------------
            # Profile Summary
            # --------------------------------------------------

            st.divider()

            st.header("ðŸ‘¤ Profile Summary")

            profile = result.get(
                "profile",
                {}
            )

            profile_col1, profile_col2 = st.columns(2)

            with profile_col1:

                st.markdown("### ðŸ’» Detected Skills")

                detected_skills = profile.get(
                    "skills",
                    []
                )

                if detected_skills:

                    st.write(
                        ", ".join(detected_skills)
                    )

                else:

                    st.info(
                        "No skills detected."
                    )


            with profile_col2:

                st.markdown("### ðŸ“ Location")

                detected_location = profile.get(
                    "location"
                )

                if detected_location:

                    st.write(
                        detected_location
                    )

                elif location:

                    st.write(
                        location
                    )

                else:

                    st.write(
                        "Not detected"
                    )


            # --------------------------------------------------
            # Education
            # --------------------------------------------------

            education = profile.get(
                "education"
            )

            if education:

                st.markdown("### ðŸŽ“ Education")

                st.write(
                    education
                )


            # --------------------------------------------------
            # Experience
            # --------------------------------------------------

            experience = profile.get(
                "experience"
            )

            if experience:

                st.markdown("### ðŸ’¼ Experience")

                st.write(
                    experience
                )


            # --------------------------------------------------
            # Projects
            # --------------------------------------------------

            projects = profile.get(
                "projects",
                []
            )

            if projects:

                st.markdown("### ðŸ› ï¸ Projects")

                if isinstance(projects, list):

                    for project in projects:

                        st.write(
                            f"â€¢ {project}"
                        )

                else:

                    st.write(
                        projects
                    )


            # --------------------------------------------------
            # Priority Skills
            # --------------------------------------------------

            st.divider()

            st.header(
                "ðŸ“ˆ Skills With Highest Opportunity"
            )

            priority_skills = result.get(
                "priority_skills",
                []
            )

            if priority_skills:

                st.caption(
                    "These are missing skills that occur across "
                    "the matched job postings."
                )

                for index, item in enumerate(
                    priority_skills[:10],
                    start=1
                ):

                    with st.container(border=True):

                        col1, col2 = st.columns([3, 1])

                        with col1:

                            st.markdown(
                                f"### {index}. "
                                f"{item.get('skill', 'N/A')}"
                            )

                        with col2:

                            st.metric(
                                "Jobs potentially unlocked",
                                item.get(
                                    "job_count",
                                    0
                                )
                            )

            else:

                st.info(
                    "No priority skills were identified."
                )

            # --------------------------------------------------
#            Gemini AI Career Reasoning
# -----------            # --------------------------------------------------
            # Gemini AI Career Reasoning
            # --------------------------------------------------

            st.divider()

            st.header("ðŸ¤– AI Career Reasoning")

            llm_analysis = result.get(
                "llm_analysis",
                {}
            )

            if llm_analysis:

                # Overall explanation
                summary = llm_analysis.get(
                    "summary"
                )

                if summary:
                    st.markdown("### ðŸ§  Career Summary")
                    st.info(summary)

                # Why specific skills are important
                priority_explanations = llm_analysis.get(
                    "priority_explanations",
                    []
                )

                if priority_explanations:
                    st.markdown(
                        "### ðŸŽ¯ Why These Skills Matter"
                    )

                    for item in priority_explanations:

                        skill = item.get(
                            "skill",
                            "Skill"
                        )

                        explanation = item.get(
                            "explanation",
                            "No explanation available."
                        )

                        with st.container(border=True):
                            st.markdown(
                                f"**{skill}**"
                            )
                            st.write(
                                explanation
                            )

                # Job-specific reasoning
                job_insights = llm_analysis.get(
                    "job_insights",
                    []
                )

                if job_insights:
                    st.markdown(
                        "### ðŸ’¼ Why These Jobs Are Relevant"
                    )

                    for insight in job_insights:

                        job_id = insight.get(
                            "job_id",
                            "Job"
                        )

                        explanation = insight.get(
                            "explanation",
                            "No explanation available."
                        )

                        with st.container(border=True):
                            st.markdown(
                                f"**Job ID: {job_id}**"
                            )
                            st.write(
                                explanation
                            )

                # Overall learning strategy
                learning_strategy = llm_analysis.get(
                    "learning_strategy"
                )

                if learning_strategy:
                    st.markdown(
                        "### ðŸ“š AI Learning Strategy"
                    )

                    st.success(
                        learning_strategy
                    )

            else:
                st.info(
                    "AI reasoning is not available "
                    "for this analysis."
                )

            
            # --------------------------------------------------
            # Job Recommendations
            # --------------------------------------------------

            st.divider()

            st.header(
                "ðŸŽ¯ Top Job Matches"
            )

            jobs = result.get(
                "jobs",
                []
            )

            if not jobs:

                st.warning(
                    "No matching jobs were found "
                    "for the selected location."
                )

            else:

                for index, job in enumerate(
                    jobs,
                    start=1
                ):

                    match_score = float(
                        job.get(
                            "match_score",
                            0
                        )
                    )

                    match_percentage = max(
                        0,
                        min(
                            100,
                            round(
                                match_score * 100,
                                1
                            )
                        )
                    )

                    gap_percentage = job.get(
                        "gap_percentage",
                        0
                    )

                    with st.container(border=True):

                        st.subheader(
                            f"{index}. "
                            f"{job.get('job_title', 'Job')}"
                        )

                        job_col1, job_col2, job_col3 = st.columns(3)

                        with job_col1:

                            st.write(
                                f"**ðŸ¢ Company:** "
                                f"{job.get('company', 'N/A')}"
                            )

                        with job_col2:

                            st.write(
                                f"**ðŸ“ Location:** "
                                f"{job.get('location', 'N/A')}"
                            )

                        with job_col3:

                            st.metric(
                                "Match",
                                f"{match_percentage}%"
                            )

                        st.write(
                            f"**Skill Gap:** "
                            f"{gap_percentage}%"
                        )

                        st.markdown(
                            "**âœ… Matched Skills**"
                        )

                        matched_skills = job.get(
                            "matched_skills",
                            []
                        )

                        if matched_skills:

                            st.write(
                                ", ".join(
                                    matched_skills
                                )
                            )

                        else:

                            st.write(
                                "No direct skill matches found."
                            )

                        st.markdown(
                            "**âš ï¸ Missing Skills**"
                        )

                        missing_skills = job.get(
                            "missing_skills",
                            []
                        )

                        if missing_skills:

                            for skill in missing_skills:

                                st.write(
                                    f"â€¢ {skill}"
                                )

                        else:

                            st.success(
                                "No major skill gaps identified."
                            )

                        # ------------------------------------------
                        # Job-specific courses
                        # ------------------------------------------

                        courses = job.get(
                            "recommended_courses",
                            []
                        )

                        if courses:

                            st.markdown(
                                "**ðŸ“š Recommended Courses for This Job**"
                            )

                            displayed_courses = []

                            for course in courses:

                                if (
                                    free_only
                                    and not is_free_course(
                                        course.get("cost")
                                    )
                                ):

                                    continue

                                displayed_courses.append(
                                    course
                                )

                            if not displayed_courses:

                                st.info(
                                    "No free courses were found "
                                    "for this job's missing skills."
                                )

                            else:

                                for course in displayed_courses[:5]:

                                    course_name = course.get(
                                        "course_name",
                                        "Course"
                                    )

                                    platform = course.get(
                                        "platform",
                                        "N/A"
                                    )

                                    opportunity = course.get(
                                        "opportunity_score",
                                        0
                                    )

                                    duration = course.get(
                                        "duration",
                                        "N/A"
                                    )

                                    duration_hours = course.get(
                                        "duration_hours",
                                        "N/A"
                                    )

                                    cost = course.get(
                                        "cost",
                                        "N/A"
                                    )

                                    st.markdown(
                                        f"**{course_name}**"
                                    )

                                    course_col1, course_col2, course_col3, course_col4 = st.columns(4)

                                    with course_col1:
                                        st.write(
                                            f"ðŸ« {platform}"
                                        )

                                    with course_col2:
                                        st.write(
                                            f"â±ï¸ {duration}"
                                        )

                                    with course_col3:
                                        st.write(
                                            f"ðŸ“š {duration_hours} hours"
                                        )

                                    with course_col4:
                                        st.write(
                                            f"ðŸ’° {cost}"
                                        )

                                    st.write(
                                        f"ðŸŽ¯ {opportunity} "
                                        f"jobs potentially unlocked"
                                    )

                                    course_url = course.get(
                                        "url"
                                    )

                                    if course_url:

                                        st.link_button(
                                            "ðŸ”— View Course",
                                            course_url
                                        )

                                    st.write("")


            # --------------------------------------------------
            # Final Summary
            # --------------------------------------------------

            st.divider()

            st.header(
                "ðŸ’¡ Career Analysis Summary"
            )

            st.info(
                f"""
                The system analyzed your resume against
                **{len(jobs)} job opportunities**.

                It identified **{len(priority_skills)} priority
                skill gaps** and generated a training path
                containing **{len(training_path)} learning steps**.

                The recommendations are based on the skills
                required by the matched job postings.

                The estimated time-to-ready is based on the
                selected courses' learning hours and your
                selected study time of **{weekly_hours} hours/week**.
                """
            )

        except Exception as error:

            st.error(
                "âŒ Something went wrong while running "
                "the Career Agent."
            )

            st.exception(error)

