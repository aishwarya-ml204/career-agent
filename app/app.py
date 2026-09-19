import sys
from pathlib import Path

import streamlit as st


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
# Header
# --------------------------------------------------

st.title("🎯 Career Agent")

st.markdown(
    """
    **AI-powered career guidance using local job opportunities,
    skill-gap analysis and personalized training paths.**

    The Career Agent:
    - 🔍 Parses your profile
    - 💼 Matches you with relevant jobs
    - 📊 Identifies missing skills
    - 📈 Ranks skills by job opportunity
    - 📚 Recommends relevant courses
    - 🛣️ Creates a personalized training path
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

    if not education and not skills and not location and not interests:

        st.warning(
            "Please enter at least some profile information."
        )

    else:

        profile_text = f"""
        I am a {education}.
        I live in {location}.
        I know {skills}.
        I am interested in {interests}.
        """

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

                st.header("📈 Skills With Highest Opportunity")

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
                                    item.get("job_count", 0)
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

                            # Job-specific courses
                            courses = job.get(
                                "recommended_courses",
                                []
                            )

                            if courses:

                                st.markdown(
                                    "**📚 Recommended Courses for This Job**"
                                )

                                for course in courses[:5]:

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

                                    st.write(
                                        f"• **{course_name}** "
                                        f"({platform}) — "
                                        f"{opportunity} jobs potentially unlocked"
                                    )

                                    course_url = course.get(
                                        "url"
                                    )

                                    if course_url:

                                        st.link_button(
                                            "View Course",
                                            course_url
                                        )


                # --------------------------------------------------
                # Personalized Training Path
                # --------------------------------------------------

                st.divider()

                st.header("🛣️ Personalized Training Path")

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

                    for item in training_path:

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

                            st.metric(
                                "Jobs potentially unlocked",
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

                st.header("💡 Career Analysis Summary")

                st.info(
                    f"""
                    The system analyzed your profile against
                    **{len(jobs)} job opportunities**.

                    It identified **{len(priority_skills)} priority
                    skill gaps** and generated a training path
                    containing **{len(training_path)} learning steps**.

                    The recommendations are based on the skills
                    required by the matched job postings.
                    """
                )


            except Exception as error:

                st.error(
                    "Something went wrong while running the Career Agent."
                )

                st.exception(error)