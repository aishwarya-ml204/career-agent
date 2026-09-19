import streamlit as st
import pandas as pd
from pathlib import Path

from agents.course_recommender import recommend_courses


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Learning Path | Career Compass",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #F7F9FC;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 35px;
        padding-bottom: 60px;
    }

    .top-title {
        color: #0B1628;
        font-size: 30px;
        font-weight: 850;
        margin-bottom: 5px;
    }

    .top-subtitle {
        color: #6F7B8F;
        font-size: 14px;
        margin-bottom: 30px;
    }

    .section-label {
        color: #356AE6;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-top: 30px;
        margin-bottom: 5px;
    }

    .section-title {
        color: #172033;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 7px;
    }

    .section-text {
        color: #6F7B8F;
        font-size: 13px;
        margin-bottom: 20px;
    }

    .summary-card {
        background: #FFFFFF;
        border: 1px solid #D9E0EA;
        border-radius: 12px;
        padding: 20px;
        min-height: 105px;
    }

    .summary-number {
        color: #172033;
        font-size: 25px;
        font-weight: 850;
    }

    .summary-label {
        color: #6F7B8F;
        font-size: 11px;
        margin-top: 5px;
    }

    .course-card {
        background: #FFFFFF;
        border: 1px solid #D9E0EA;
        border-radius: 12px;
        padding: 20px;
        min-height: 205px;
        margin-bottom: 10px;
    }

    .course-platform {
        color: #356AE6;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.7px;
        text-transform: uppercase;
    }

    .course-title {
        color: #172033;
        font-size: 16px;
        font-weight: 800;
        line-height: 1.35;
        margin-top: 10px;
    }

    .course-meta {
        color: #6F7B8F;
        font-size: 11px;
        margin-top: 12px;
    }

    .course-skills {
        color: #6F7B8F;
        font-size: 11px;
        line-height: 1.5;
        margin-top: 8px;
    }

    .free-header {
        color: #1E9B68;
        font-size: 20px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .paid-header {
        color: #D9822B;
        font-size: 20px;
        font-weight: 800;
        margin-top: 35px;
        margin-bottom: 15px;
    }

    .info-box {
        background: #FFFFFF;
        border: 1px solid #D9E0EA;
        border-left: 4px solid #356AE6;
        border-radius: 10px;
        padding: 18px;
        color: #56627A;
        font-size: 12px;
        line-height: 1.6;
        margin-top: 20px;
    }

    .footer {
        text-align: center;
        color: #929CAD;
        font-size: 11px;
        margin-top: 50px;
        padding-top: 25px;
        border-top: 1px solid #D9E0EA;
    }

    div[data-testid="stButton"] > button {
        border-radius: 8px !important;
        min-height: 42px !important;
        font-weight: 750 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="top-title">Personalized Learning Path</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="top-subtitle">'
    'Build the skills that can improve your alignment with your target opportunities.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# GET CAREER RESULT
# ============================================================

result = st.session_state.get("career_result")

selected_job = st.session_state.get("selected_job")


# ============================================================
# RECOVER RESULT IF NEEDED
# ============================================================

if not result:

    profile_input = st.session_state.get(
        "profile_input",
        {}
    )

    if profile_input:

        try:

            from agents.career_pipeline import run_career_analysis

            education = profile_input.get(
                "education",
                ""
            )

            location = profile_input.get(
                "location",
                ""
            )

            skills = profile_input.get(
                "skills",
                ""
            )

            interests = profile_input.get(
                "interests",
                ""
            )

            profile_text = f"""
I am a {education}.
I live in {location}.
I know {skills}.
I am interested in {interests}.
"""

            result = run_career_analysis(
                profile_text,
                top_k=5
            )

            st.session_state["career_result"] = result

        except Exception as e:

            st.error(
                f"Unable to rebuild your career analysis: {e}"
            )

            st.stop()

    else:

        st.warning(
            "Please complete your profile and career analysis first."
        )

        if st.button(
            "← Go to Profile",
            type="primary"
        ):
            st.switch_page(
                "pages/profile.py"
            )

        st.stop()


# ============================================================
# GET JOBS
# ============================================================

jobs = result.get(
    "jobs",
    []
)


# ============================================================
# COLLECT SKILL GAPS
# ============================================================

missing_skills = []
matched_skills = []

for job in jobs:

    missing = job.get(
        "missing_skills",
        []
    )

    matched = job.get(
        "matched_skills",
        []
    )

    if isinstance(missing, str):

        missing = [
            x.strip()
            for x in missing.split(",")
            if x.strip()
        ]

    if isinstance(matched, str):

        matched = [
            x.strip()
            for x in matched.split(",")
            if x.strip()
        ]

    missing_skills.extend(missing)
    matched_skills.extend(matched)


# Remove duplicates while preserving order

missing_unique = list(
    dict.fromkeys(
        missing_skills
    )
)

matched_unique = list(
    dict.fromkeys(
        matched_skills
    )
)


# ============================================================
# IF A JOB WAS SELECTED
# ============================================================

if selected_job:

    selected_missing = selected_job.get(
        "missing_skills",
        []
    )

    if isinstance(selected_missing, str):

        selected_missing = [
            x.strip()
            for x in selected_missing.split(",")
            if x.strip()
        ]

    if selected_missing:

        missing_unique = list(
            dict.fromkeys(
                selected_missing
                + missing_unique
            )
        )


# ============================================================
# SUMMARY
# ============================================================

st.markdown(
    '<div class="section-label">YOUR DEVELOPMENT PLAN</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Skills to build</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-text">'
    'These skills are identified from your matched job opportunities.'
    '</div>',
    unsafe_allow_html=True
)


s1, s2, s3 = st.columns(3)


with s1:

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-number">
                {len(missing_unique)}
            </div>
            <div class="summary-label">
                SKILLS TO DEVELOP
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with s2:

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-number">
                {len(matched_unique)}
            </div>
            <div class="summary-label">
                SKILLS ALREADY MATCHED
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with s3:

    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-number">
                {len(jobs)}
            </div>
            <div class="summary-label">
                TARGET OPPORTUNITIES
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SKILLS
# ============================================================

if missing_unique:

    st.markdown(
        '<div class="section-label">PRIORITY SKILLS</div>',
        unsafe_allow_html=True
    )

    skills_html = ""

    for skill in missing_unique:

        skills_html += f"""
        <span style="
            display:inline-block;
            background:#FFF4E8;
            color:#A85E12;
            border:1px solid #F0D5B5;
            padding:7px 11px;
            border-radius:6px;
            margin:4px;
            font-size:11px;
            font-weight:700;
        ">
            + {skill}
        </span>
        """

    st.markdown(
        f"""
        <div style="
            background:#FFFFFF;
            border:1px solid #D9E0EA;
            border-radius:12px;
            padding:18px;
        ">
            {skills_html}
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "No major skill gaps were detected from the current job matches."
    )


# ============================================================
# RECOMMEND COURSES
# ============================================================

try:

    courses = recommend_courses(
        missing_unique,
        top_k=10
    )

except Exception as e:

    st.error(
        f"Unable to load recommended courses: {e}"
    )

    courses = []


# ============================================================
# NORMALIZE COURSES
# ============================================================

normalised_courses = []

for course in courses:

    if isinstance(course, dict):

        normalised_courses.append(course)

    else:

        try:

            normalised_courses.append(
                dict(course)
            )

        except Exception:

            continue


# ============================================================
# COURSE CLASSIFICATION
# ============================================================

free_courses = []
paid_courses = []

for course in normalised_courses:

    course_name = str(
        course.get("course_name", "")
    ).lower()

    platform = str(
        course.get("platform", "")
    ).lower()

    # FREE LEARNING RESOURCES
    if (
        "kaggle" in platform
        or "kaggle" in course_name
        or (
            "deeplearning.ai" in platform
            and (
                "short course" in course_name
                or "langchain" in course_name
                or "rag" in course_name
            )
        )
    ):

        free_courses.append(course)

    # PAID PROGRAMS / CERTIFICATES
    elif (
        "coursera" in platform
        or "deep learning specialization" in course_name
        or "professional certificate" in course_name
    ):

        paid_courses.append(course)

    else:
        # If a future course cannot be classified,
        # don't show it in the main sections.
        continue

    
def render_course_card(course):

    course_name = course.get(
        "course_name",
        "Recommended Course"
    )

    platform = course.get(
        "platform",
        "Learning Platform"
    )

    level = course.get(
        "level",
        "All Levels"
    )

    duration = course.get(
        "duration",
        "Duration not specified"
    )

    skills = course.get(
        "skills",
        ""
    )

    url = course.get(
        "url",
        ""
    )

    # Convert skill list into readable text
    if isinstance(skills, list):
        skills = ", ".join(
            str(skill)
            for skill in skills
        )

    # --------------------------------------------------------
    # COURSE CARD
    # --------------------------------------------------------

    with st.container(border=True):

        st.caption(
            str(platform).upper()
        )

        st.markdown(
            f"### {course_name}"
        )

        st.write(
            f"**Level:** {level}   •   "
            f"**Duration:** {duration}"
        )

        st.write(
            f"**Skills:** {skills}"
        )

        if url:

            st.link_button(
                "Explore Course →",
                url,
                use_container_width=True
            )
# ============================================================
# FREE COURSES
# ============================================================

st.markdown(
    '<div class="free-header">FREE COURSES</div>',
    unsafe_allow_html=True
)

if free_courses:

    cols = st.columns(2)

    for index, course in enumerate(free_courses):

        with cols[index % 2]:

            render_course_card(
                course
            )

else:

    st.info(
    "No free courses matched your current skill gaps."
)


# ============================================================
# PAID COURSES
# ============================================================

st.markdown(
    '<div class="paid-header">PAID COURSES</div>',
    unsafe_allow_html=True
)

if paid_courses:

    cols = st.columns(2)

    for index, course in enumerate(paid_courses):

        with cols[index % 2]:

            render_course_card(
                course
            )

else:

    st.info(
    "No paid courses matched your current skill gaps."
)




# ============================================================
# NO COURSES
# ============================================================

if not normalised_courses:

    st.markdown(
        """
        <div class="info-box">
            No course recommendations were returned for the
            current skill gaps. Try adding more technical skills
            to your profile or selecting a different opportunity.
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# NAVIGATION
# ============================================================

st.write("")
st.write("")

c1, c2, c3 = st.columns(
    [1, 2, 1]
)

with c1:

    if st.button(
        "← Skill Gap",
        use_container_width=True
    ):

        st.switch_page(
            "pages/skill_gaps.py"
        )


with c3:

    if st.button(
        "← Update Profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/profile.py"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Career Compass · Intelligent Career Navigation
    </div>
    """,
    unsafe_allow_html=True
)