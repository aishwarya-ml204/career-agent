import streamlit as st

st.set_page_config(
    page_title="Career Compass",
    page_icon="🧭",
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
    icon="🏠"
)

profile = st.Page(
    "pages/profile.py",
    title="Profile",
    icon="👤"
)

analysis = st.Page(
    "pages/analysis.py",
    title="AI Analysis",
    icon="🤖"
)

jobs = st.Page(
    "pages/jobs.py",
    title="Jobs",
    icon="💼"
)

job_details = st.Page(
    "pages/job_details.py",
    title="Job Details",
    icon="📄"
)

skill_gaps = st.Page(
    "pages/skill_gaps.py",
    title="Skill Gaps",
    icon="🎯"
)

learning = st.Page(
    "pages/learning_path.py",
    title="Learning Path",
    icon="📚"
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

st.header("👤 Candidate Profile")

resume_file = st.file_uploader(
    "📄 Upload Your Resume",
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
        "📍 Preferred Job Location",
        placeholder="Example: Bengaluru, Karnataka"
    )

with col2:
    interests = st.text_input(
        "❤️ Career Interests",
        placeholder="Example: Machine Learning, Data Science"
    )


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

    if resume_file is None:
        st.warning(
            "📄 Please upload your resume first."
        )

    else:

        try:

            # ------------------------------------------
            # Extract resume text
            # ------------------------------------------

            with st.spinner("📄 Reading your resume..."):

                resume_text = extract_text_from_resume(
                    resume_file
                )

            if not resume_text or not resume_text.strip():

                st.error(
                    "❌ Could not extract text from this resume. "
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
                "🔄 Analyzing your resume and finding opportunities..."
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

                st.markdown("### 🎓 Education")

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

                st.markdown("### 💼 Experience")

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

                st.markdown("### 🛠️ Projects")

                if isinstance(projects, list):

                    for project in projects:

                        st.write(
                            f"• {project}"
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
                "📈 Skills With Highest Opportunity"
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

            st.header("🤖 AI Career Reasoning")

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
                    st.markdown("### 🧠 Career Summary")
                    st.info(summary)

                # Why specific skills are important
                priority_explanations = llm_analysis.get(
                    "priority_explanations",
                    []
                )

                if priority_explanations:
                    st.markdown(
                        "### 🎯 Why These Skills Matter"
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
                        "### 💼 Why These Jobs Are Relevant"
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
                        "### 📚 AI Learning Strategy"
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
                "🎯 Top Job Matches"
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
                                        f"🎯 {opportunity} "
                                        f"jobs potentially unlocked"
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
                    "Courses are selected for the "
                    "highest-priority missing skills."
                )

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

                total_hours = calculate_time_to_ready(
                    filtered_training_path
                )

                ready_days = (
                    (total_hours / weekly_hours) * 7
                    if weekly_hours > 0
                    else 0
                )

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
                        "No courses remain after applying "
                        "the selected filter."
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
                "❌ Something went wrong while running "
                "the Career Agent."
            )

            st.exception(error)
>>>>>>> 62f8016 (Add Gemini career reasoning and retry handling)
