# Streamlit application
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
    **AI-powered career guidance for skill-gap analysis and job matching**

    Enter your profile details below. The Career Agent will:
    - 🔍 Understand your profile
    - 💼 Find relevant jobs
    - 📊 Analyze your skill gaps
    - 📚 Recommend training courses
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
        "💻 Skills",
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

        # Combine all profile infoprofile_text = f"""rmation
        
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
                        "courses": []
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

                    for index, job in enumerate(jobs, start=1):

                        match_score = float(
                            job.get(
                                "match_score",
                                0
                            )
                        )

                        # Convert similarity to percentage
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

                        with st.container(border=True):

                            st.subheader(
                                f"{index}. {job.get('job_title', 'Job')}"
                            )

                            job_col1, job_col2 = st.columns(2)

                            with job_col1:

                                st.write(
                                    f"**🏢 Company:** "
                                    f"{job.get('company', 'N/A')}"
                                )

                                st.write(
                                    f"**📍 Location:** "
                                    f"{job.get('location', 'N/A')}"
                                )

                            with job_col2:

                                st.metric(
                                    "Match",
                                    f"{match_percentage}%"
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


                # --------------------------------------------------
                # Course Recommendations
                # --------------------------------------------------

                st.divider()

                st.header("📚 Recommended Training")

                courses = result.get(
                    "courses",
                    []
                )

                if not courses:

                    st.info(
                        "No course recommendations available."
                    )

                else:

                    for index, course in enumerate(
                        courses,
                        start=1
                    ):

                        with st.container(border=True):

                            st.subheader(
                                f"{index}. "
                                f"{course.get('course_name', 'Course')}"
                            )

                            course_col1, course_col2 = st.columns(2)

                            with course_col1:

                                st.write(
                                    f"**Platform:** "
                                    f"{course.get('platform', 'N/A')}"
                                )

                                st.write(
                                    f"**Level:** "
                                    f"{course.get('level', 'N/A')}"
                                )

                            with course_col2:

                                st.write(
                                    f"**Duration:** "
                                    f"{course.get('duration', 'N/A')}"
                                )

                            recommended_skills = course.get(
                                "skills",
                                []
                            )

                            if recommended_skills:

                                st.write(
                                    "**Skills covered:** "
                                    + ", ".join(
                                        recommended_skills
                                    )
                                )

                            course_url = course.get(
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

                st.header("💡 Career Summary")

                if jobs:

                    best_job = jobs[0]

                    st.info(
                        f"""
                        Based on your current profile, the system identified
                        **{len(jobs)} relevant job opportunities**.

                        Your top matching role is:

                        **{best_job.get('job_title', 'N/A')}**

                        The system also identified skill gaps and retrieved
                        training resources to help you prepare for these roles.
                        """
                    )

            except Exception as error:

                st.error(
                    "Something went wrong while running the Career Agent."
                )

                st.exception(error)