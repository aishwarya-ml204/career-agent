import sys
from pathlib import Path

import streamlit as st
from pypdf import PdfReader


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from workflow.graph import build_graph


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Career Agent",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def is_free_course(cost):
    """Return True if the course is free."""

    if cost is None:
        return False

    return str(cost).strip().lower() in [
        "free",
        "0",
        "0.0",
        "$0",
        "₹0"
    ]


def get_duration_hours(course):
    """Safely convert duration hours to a number."""

    value = course.get("duration_hours")

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def calculate_time_to_ready(training_path):
    """
    Calculate total learning hours for the
    selected training path.

    Courses with unknown duration are not
    included in the numerical total.
    """

    total_hours = 0

    for course in training_path:

        hours = get_duration_hours(course)

        if hours is not None:
            total_hours += hours

    return total_hours


def format_hours(hours):
    """Display hours cleanly."""

    if hours == int(hours):
        return str(int(hours))

    return f"{hours:.1f}"


def extract_resume_text(uploaded_file):
    """Extract text from an uploaded PDF resume."""

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🎯 Career Agent")

st.markdown(
    """
    **AI-powered career guidance using local job opportunities,
    skill-gap analysis and personalized training paths.**

    The Career Agent:
    - 🔍 Parses your profile
    - 📄 Reads your resume
    - 💼 Matches you with relevant jobs
    - 📊 Identifies missing skills
    - 📈 Ranks skills by job opportunity
    - 📚 Recommends relevant courses
    - 🛣️ Creates a personalized training path
    - ⏱️ Estimates time needed to become job-ready
    """
)

st.divider()


# --------------------------------------------------
# Candidate Profile
# --------------------------------------------------

st.header("👤 Candidate Profile")

col1, col2 = st.columns(2)

with col1:

    education = st.text_input(
        "🎓 Education",
        placeholder="Example: B.Tech Computer Science"
    )

    skills = st.text_input(
        "💻 Current Skills",
        placeholder="Example: Python, SQL, Pandas, NumPy"
    )


with col2:

    location = st.text_input(
        "📍 Location",
        placeholder="Example: Bengaluru, Karnataka"
    )

    interests = st.text_input(
        "❤️ Interests",
        placeholder="Example: Machine Learning, Data Science"
    )


# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

st.subheader("📄 Resume Upload")

uploaded_resume = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)

if uploaded_resume:

    st.success(
        f"Resume uploaded: {uploaded_resume.name}"
    )

    try:

        resume_text = extract_resume_text(
            uploaded_resume
        )

        if resume_text.strip():

            with st.expander("👀 View extracted resume text"):

                st.text_area(
                    "Resume Text",
                    resume_text,
                    height=250
                )

        else:

            st.warning(
                "No readable text was found in the PDF."
            )

    except Exception as error:

        st.error(
            "Unable to read the uploaded PDF."
        )

        st.exception(error)


st.write("")


# --------------------------------------------------
# Training Preferences
# --------------------------------------------------

st.header("⚙️ Training Preferences")

pref_col1, pref_col2 = st.columns(2)

with pref_col1:

    free_only = st.checkbox(
        "🆓 Show only free courses"
    )

with pref_col2:

    weekly_hours = st.number_input(
        "⏰ Study hours per week",
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
    "🚀 Analyze My Career",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# Career Analysis
# --------------------------------------------------

if analyze_button:

    if (
        not education
        and not skills
        and not location
        and not interests
        and not uploaded_resume
    ):

        st.warning(
            "Please enter some profile information or upload a resume."
        )

    else:

        # ----------------------------------------------
        # Extract resume text
        # ----------------------------------------------

        resume_text = ""

        if uploaded_resume:

            try:

                resume_text = extract_resume_text(
                    uploaded_resume
                )

            except Exception as error:

                st.error(
                    "Could not extract text from the uploaded resume."
                )

                st.exception(error)


        # ----------------------------------------------
        # Create profile text
        # ----------------------------------------------

        profile_text = f"""
        I am a {education}.
        I live in {location}.
        I know {skills}.
        I am interested in {interests}.

        Resume information:
        {resume_text}
        """


        # ----------------------------------------------
        # Run Career Agent
        # ----------------------------------------------

        with st.spinner(
            "🔄 Analyzing your profile and finding opportunities..."
        ):

            try:

                # Build LangGraph workflow
                career_graph = build_graph()

                # Run workflow
                result = career_graph.invoke(
                    {
                        "profile_text": profile_text,
                        "profile": {},
                        "jobs": [],
                        "priority_skills": [],
                        "training_path": []
                    }
                )

                st.success(
                    "Career analysis completed successfully! 🎉"
                )


                # --------------------------------------------------
                # Profile Summary
                # --------------------------------------------------

                st.divider()

                st.header("👤 Profile Summary")

                profile = result.get(
                    "profile",
                    {}
                )

                profile_col1, profile_col2 = st.columns(2)

                with profile_col1:

                    st.markdown("### 💻 Detected Skills")

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

                    st.markdown("### 📍 Location")

                    detected_location = profile.get(
                        "location"
                    )

                    st.write(
                        detected_location
                        if detected_location
                        else "Not detected"
                    )


                # --------------------------------------------------
                # Priority Skills
                # --------------------------------------------------

                st.divider()

                st.header(
                    "📈 Skills With Highest Opportunity"
                )

                priority_skills = result.get(
                    "priority_skills",
                    []
                )

                if priority_skills:

                    st.caption(
                        "These are missing skills that occur across the matched job postings."
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
                # Job Recommendations
                # --------------------------------------------------

                st.divider()

                st.header("🎯 Top Job Matches")

                jobs = result.get(
                    "jobs",
                    []
                )

                if not jobs:

                    st.warning(
                        "No matching jobs were found for the selected location."
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
                                    f"**🏢 Company:** "
                                    f"{job.get('company', 'N/A')}"
                                )

                            with job_col2:

                                st.write(
                                    f"**📍 Location:** "
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
                                "**✅ Matched Skills**"
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
                                "**⚠️ Missing Skills**"
                            )

                            missing_skills = job.get(
                                "missing_skills",
                                []
                            )

                            if missing_skills:

                                for skill in missing_skills:

                                    st.write(
                                        f"• {skill}"
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
                                    "**📚 Recommended Courses for This Job**"
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
                                        "No free courses were found for "
                                        "this job's missing skills."
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
                                                f"🏫 {platform}"
                                            )

                                        with course_col2:

                                            st.write(
                                                f"⏱️ {duration}"
                                            )

                                        with course_col3:

                                            st.write(
                                                f"📚 {duration_hours} hours"
                                            )

                                        with course_col4:

                                            st.write(
                                                f"💰 {cost}"
                                            )

                                        st.write(
                                            f"🎯 {opportunity} jobs potentially unlocked"
                                        )

                                        course_url = course.get(
                                            "url"
                                        )

                                        if course_url:

                                            st.link_button(
                                                "🔗 View Course",
                                                course_url
                                            )

                                        st.write("")


                # --------------------------------------------------
                # Personalized Training Path
                # --------------------------------------------------

                st.divider()

                st.header(
                    "🛣️ Personalized Training Path"
                )

                training_path = result.get(
                    "training_path",
                    []
                )

                if not training_path:

                    st.info(
                        "No training path could be generated."
                    )

                else:

                    st.caption(
                        "Courses are selected for the highest-priority missing skills."
                    )

                    # ----------------------------------------------
                    # Filter training path
                    # ----------------------------------------------

                    filtered_training_path = []

                    for item in training_path:

                        if free_only:

                            if not is_free_course(
                                item.get("cost")
                            ):

                                continue

                        filtered_training_path.append(
                            item
                        )


                    # ----------------------------------------------
                    # Time-to-ready calculation
                    # ----------------------------------------------

                    total_hours = calculate_time_to_ready(
                        filtered_training_path
                    )

                    ready_days = (
                        (total_hours / weekly_hours) * 7
                        if weekly_hours > 0
                        else 0
                    )


                    # ----------------------------------------------
                    # Training summary metrics
                    # ----------------------------------------------

                    summary_col1, summary_col2, summary_col3 = st.columns(3)

                    with summary_col1:

                        st.metric(
                            "Training Hours",
                            format_hours(total_hours)
                        )

                    with summary_col2:

                        st.metric(
                            "Estimated Time-to-Ready",
                            f"{ready_days:.1f} days"
                        )

                    with summary_col3:

                        free_count = sum(
                            1
                            for item in filtered_training_path
                            if is_free_course(
                                item.get("cost")
                            )
                        )

                        st.metric(
                            "Free Courses",
                            free_count
                        )


                    if free_only:

                        st.info(
                            "🆓 Free-only filter is active. "
                            "Paid courses have been excluded."
                        )


                    if not filtered_training_path:

                        st.warning(
                            "No courses remain after applying the "
                            "selected filter."
                        )

                    else:

                        for item in filtered_training_path:

                            with st.container(border=True):

                                st.subheader(
                                    f"Step {item.get('step', '')}: "
                                    f"{item.get('skill', 'Skill')}"
                                )

                                st.write(
                                    f"**📚 Course:** "
                                    f"{item.get('course_name', 'N/A')}"
                                )

                                st.write(
                                    f"**🏫 Platform:** "
                                    f"{item.get('platform', 'N/A')}"
                                )

                                st.write(
                                    f"**📊 Level:** "
                                    f"{item.get('level', 'N/A')}"
                                )

                                st.write(
                                    f"**⏱️ Duration:** "
                                    f"{item.get('duration', 'N/A')}"
                                )

                                st.write(
                                    f"**📚 Learning Hours:** "
                                    f"{item.get('duration_hours', 'N/A')}"
                                )

                                st.write(
                                    f"**💰 Cost:** "
                                    f"{item.get('cost', 'N/A')}"
                                )

                                st.metric(
                                    "🎯 Jobs potentially unlocked",
                                    item.get(
                                        "jobs_unlocked",
                                        0
                                    )
                                )

                                course_url = item.get(
                                    "url"
                                )

                                if course_url:

                                    st.link_button(
                                        "🔗 View Course",
                                        course_url
                                    )


                # --------------------------------------------------
                # Final Summary
                # --------------------------------------------------

                st.divider()

                st.header(
                    "💡 Career Analysis Summary"
                )

                st.info(
                    f"""
                    The system analyzed your profile against
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
                    "Something went wrong while running the Career Agent."
                )

                st.exception(error)