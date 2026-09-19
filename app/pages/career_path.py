import streamlit as st
import textwrap

from agents.course_recommender import recommend_courses


# ============================================================
# HTML HELPER
# ============================================================

def render_html(html):
    st.html(textwrap.dedent(html).strip())


# ============================================================
# PROFESSIONAL DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background: #F7F9FC;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 0.8rem;
        padding-bottom: 4rem;
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


    /* ======================================================
       NAVIGATION
       ====================================================== */

    .top-nav {
        width: 100%;
        min-height: 66px;

        display: flex;
        align-items: center;
        justify-content: space-between;

        border-bottom: 1px solid #E5E9F0;
        margin-bottom: 35px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-icon {
        width: 38px;
        height: 38px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #0B1628;
        border-radius: 10px;

        color: white;
        font-size: 18px;
    }

    .brand-name {
        color: #101A2B;
        font-size: 17px;
        font-weight: 850;
    }

    .brand-subtitle {
        color: #8791A2;
        font-size: 9px;
        margin-top: 2px;
        letter-spacing: 0.5px;
    }

    .page-label {
        background: #EEF3FF;
        color: #356AE6;

        padding: 9px 14px;

        border-radius: 8px;

        font-size: 10px;
        font-weight: 850;
    }


    /* ======================================================
       HEADER
       ====================================================== */

    .eyebrow {
        color: #356AE6;

        font-size: 10px;
        font-weight: 900;

        letter-spacing: 1.6px;

        margin-bottom: 8px;
    }

    .page-title {
        color: #101A2B;

        font-size: 36px;
        font-weight: 900;

        letter-spacing: -1.2px;
    }

    .page-description {
        color: #758095;

        font-size: 13px;
        line-height: 1.7;

        max-width: 720px;

        margin-top: 8px;
    }


    /* ======================================================
       PROFILE CARD
       ====================================================== */

    .profile-card {
        background: #FFFFFF;

        border: 1px solid #E1E6EE;

        border-radius: 17px;

        padding: 25px;

        margin-top: 30px;
        margin-bottom: 42px;

        box-shadow:
            0 8px 28px rgba(25, 40, 65, 0.04);
    }

    .profile-title {
        color: #182338;

        font-size: 15px;
        font-weight: 850;

        margin-bottom: 18px;
    }

    .profile-item {
        background: #F7F9FC;

        border: 1px solid #E7EBF2;

        border-radius: 10px;

        padding: 13px 15px;

        min-height: 66px;
    }

    .profile-label {
        color: #8A94A5;

        font-size: 8px;
        font-weight: 900;

        letter-spacing: 0.9px;
    }

    .profile-value {
        color: #253149;

        font-size: 12px;
        font-weight: 750;

        margin-top: 5px;
    }


    /* ======================================================
       SECTION HEADERS
       ====================================================== */

    .section {
        margin-top: 45px;
        margin-bottom: 20px;
    }

    .section-title {
        color: #101A2B;

        font-size: 25px;
        font-weight: 880;

        letter-spacing: -0.6px;
    }

    .section-text {
        color: #788398;

        font-size: 12px;

        margin-top: 6px;
    }


    /* ======================================================
       JOB CARD
       ====================================================== */

    .job-card {
        background: #FFFFFF;

        border: 1px solid #DFE5EE;

        border-radius: 16px;

        padding: 23px;

        margin-bottom: 16px;

        box-shadow:
            0 7px 22px rgba(25, 40, 65, 0.035);
    }

    .job-header {
        display: flex;

        justify-content: space-between;

        align-items: flex-start;

        gap: 20px;
    }

    .job-title {
        color: #162238;

        font-size: 17px;
        font-weight: 880;
    }

    .company {
        color: #5E6A7E;

        font-size: 12px;
        font-weight: 700;

        margin-top: 5px;
    }

    .location {
        color: #8A94A5;

        font-size: 10px;

        margin-top: 5px;
    }

    .match-box {
        min-width: 82px;

        text-align: center;

        background: #EEF8F3;

        border: 1px solid #D3EDDF;

        border-radius: 10px;

        padding: 9px 10px;
    }

    .match-number {
        color: #16855A;

        font-size: 18px;
        font-weight: 900;
    }

    .match-label {
        color: #4B856F;

        font-size: 7px;
        font-weight: 900;

        letter-spacing: 0.7px;
    }

    .job-divider {
        height: 1px;

        background: #EDF0F4;

        margin: 18px 0;
    }

    .skill-heading {
        color: #677286;

        font-size: 9px;
        font-weight: 900;

        letter-spacing: 0.7px;

        margin-bottom: 8px;
    }

    .skill-row {
        display: flex;

        flex-wrap: wrap;

        gap: 6px;
    }

    .skill-good {
        display: inline-block;

        background: #EEF8F3;

        color: #16855A;

        border: 1px solid #D6EDE1;

        padding: 5px 9px;

        border-radius: 6px;

        font-size: 9px;
        font-weight: 750;
    }

    .skill-missing {
        display: inline-block;

        background: #FFF7EC;

        color: #B76A17;

        border: 1px solid #F2DFC2;

        padding: 5px 9px;

        border-radius: 6px;

        font-size: 9px;
        font-weight: 750;
    }

    .why-box {
        background: #F7F9FC;

        border-left: 3px solid #356AE6;

        border-radius: 6px;

        padding: 10px 12px;

        margin-top: 15px;
    }

    .why-title {
        color: #356AE6;

        font-size: 9px;
        font-weight: 900;
    }

    .why-text {
        color: #687489;

        font-size: 10px;

        line-height: 1.6;

        margin-top: 3px;
    }


    /* ======================================================
       SKILL GAP
       ====================================================== */

    .gap-card {
        background: #FFFFFF;

        border: 1px solid #E1E6EE;

        border-radius: 16px;

        padding: 25px;

        box-shadow:
            0 7px 22px rgba(25, 40, 65, 0.035);
    }

    .gap-stat {
        background: #F7F9FC;

        border-radius: 10px;

        padding: 15px;
    }

    .gap-stat-number {
        color: #182338;

        font-size: 22px;
        font-weight: 900;
    }

    .gap-stat-label {
        color: #8A94A5;

        font-size: 9px;

        margin-top: 3px;
    }

    .gap-progress {
        width: 100%;

        height: 7px;

        background: #E8ECF2;

        border-radius: 20px;

        margin-top: 18px;

        overflow: hidden;
    }

    .gap-progress-fill {
        height: 100%;

        background:
            linear-gradient(
                90deg,
                #356AE6,
                #6C63FF
            );

        border-radius: 20px;
    }


    /* ======================================================
       COURSE CARDS
       ====================================================== */

    .course-card {
        background: #FFFFFF;

        border: 1px solid #E1E6EE;

        border-radius: 14px;

        padding: 20px;

        min-height: 170px;

        box-shadow:
            0 7px 22px rgba(25, 40, 65, 0.03);
    }

    .course-platform {
        color: #356AE6;

        font-size: 8px;
        font-weight: 900;

        letter-spacing: 0.8px;
    }

    .course-title {
        color: #1B263A;

        font-size: 14px;
        font-weight: 850;

        margin-top: 10px;

        line-height: 1.35;
    }

    .course-level {
        display: inline-block;

        color: #667188;

        background: #F3F5F8;

        padding: 4px 7px;

        border-radius: 5px;

        font-size: 8px;

        margin-top: 12px;
    }

    .course-duration {
        color: #8791A2;

        font-size: 9px;

        margin-top: 9px;
    }


    /* ======================================================
       BUTTON
       ====================================================== */

    div[data-testid="stButton"] > button {
        border-radius: 8px !important;

        min-height: 44px !important;

        font-weight: 800 !important;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;

        color: #929CAD;

        font-size: 10px;

        padding-top: 30px;

        margin-top: 60px;

        border-top: 1px solid #E1E6EE;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP NAV
# ============================================================

render_html(
    """
    <div class="top-nav">

        <div class="brand">

            <div class="brand-icon">
                🧭
            </div>

            <div>

                <div class="brand-name">
                    Career Compass
                </div>

                <div class="brand-subtitle">
                    INTELLIGENT CAREER NAVIGATION
                </div>

            </div>

        </div>

        <div class="page-label">
            CAREER ANALYSIS
        </div>

    </div>
    """
)


# ============================================================
# GET RESULT
# ============================================================

result = st.session_state.get(
    "career_result"
)


profile_input = st.session_state.get(
    "profile_input",
    {}
)


if not result:

    render_html(
        """
        <div style="
            background:#FFFFFF;
            border:1px solid #E1E6EE;
            border-radius:16px;
            padding:45px;
            text-align:center;
        ">

            <div style="
                color:#101A2B;
                font-size:23px;
                font-weight:850;
            ">
                No career analysis yet
            </div>

            <div style="
                color:#7A8597;
                font-size:12px;
                margin-top:8px;
            ">
                Build your profile first to generate your
                personalized career path.
            </div>

        </div>
        """
    )

    if st.button(
        "← Back to Profile",
        use_container_width=False
    ):
        st.switch_page(
            "pages/home.py"
        )

    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

render_html(
    """
    <div class="eyebrow">
        PERSONALIZED ANALYSIS
    </div>

    <div class="page-title">
        Your career path
    </div>

    <div class="page-description">
        We've analyzed your profile against relevant
        opportunities, identified skill gaps, and created
        a focused learning direction.
    </div>
    """
)


# ============================================================
# PROFILE OVERVIEW
# ============================================================

education = profile_input.get(
    "education",
    "Not specified"
)

location = profile_input.get(
    "location",
    result.get("profile", {}).get(
        "location",
        "Not specified"
    )
)

skills = profile_input.get(
    "skills",
    ""
)

interests = profile_input.get(
    "interests",
    "Not specified"
)


skill_list = [
    skill.strip()
    for skill in skills.split(",")
    if skill.strip()
]


render_html(
    f"""
    <div class="profile-card">

        <div class="profile-title">
            Profile overview
        </div>

    </div>
    """
)


p1, p2, p3 = st.columns(3, gap="medium")


with p1:

    render_html(
        f"""
        <div class="profile-item">

            <div class="profile-label">
                EDUCATION
            </div>

            <div class="profile-value">
                {education}
            </div>

        </div>
        """
    )


with p2:

    render_html(
        f"""
        <div class="profile-item">

            <div class="profile-label">
                LOCATION
            </div>

            <div class="profile-value">
                {location}
            </div>

        </div>
        """
    )


with p3:

    render_html(
        f"""
        <div class="profile-item">

            <div class="profile-label">
                INTERESTS
            </div>

            <div class="profile-value">
                {interests}
            </div>

        </div>
        """
    )


# ============================================================
# DETECTED SKILLS
# ============================================================

if skill_list:

    st.write("")

    render_html(
        """
        <div style="
            color:#8A94A5;
            font-size:9px;
            font-weight:900;
            letter-spacing:0.8px;
            margin-bottom:8px;
        ">
            YOUR CURRENT SKILLS
        </div>
        """
    )

    skill_html = ""

    for skill in skill_list:

        skill_html += f"""
        <span class="skill-good">
            {skill}
        </span>
        """

    render_html(
        f"""
        <div class="skill-row">
            {skill_html}
        </div>
        """
    )


# ============================================================
# JOB MATCHES
# ============================================================

jobs = result.get(
    "jobs",
    []
)


render_html(
    """
    <div class="section">

        <div class="eyebrow">
            STEP 03
        </div>

        <div class="section-title">
            Job matches
        </div>

        <div class="section-text">
            Opportunities ranked according to how closely
            your current skills align with their requirements.
        </div>

    </div>
    """
)


if not jobs:

    render_html(
        """
        <div style="
            background:#FFFFFF;
            border:1px dashed #CBD4E1;
            border-radius:14px;
            padding:35px;
            text-align:center;
        ">

            <div style="
                color:#536078;
                font-size:13px;
                font-weight:750;
            ">
                No job matches were returned.
            </div>

            <div style="
                color:#8A94A5;
                font-size:10px;
                margin-top:6px;
            ">
                Try adding more technical skills to your profile.
            </div>

        </div>
        """
    )

else:

    for job in jobs:

        job_title = job.get(
            "job_title",
            "Untitled Role"
        )

        company = job.get(
            "company",
            "Company"
        )

        job_location = job.get(
            "location",
            "Location not specified"
        )

        score = float(
            job.get(
                "match_score",
                0
            )
        )

        matched = job.get(
            "matched_skills",
            []
        )

        missing = job.get(
            "missing_skills",
            []
        )

        required = job.get(
            "required_skills",
            ""
        )


        # ----------------------------------------------------
        # Convert strings to lists
        # ----------------------------------------------------

        if isinstance(matched, str):

            matched = [
                x.strip()
                for x in matched.split(",")
                if x.strip()
            ]


        if isinstance(missing, str):

            missing = [
                x.strip()
                for x in missing.split(",")
                if x.strip()
            ]


        # ----------------------------------------------------
        # Why this matches
        # ----------------------------------------------------

        if matched:

            matched_text = ", ".join(
                matched[:4]
            )

            why_text = (
                f"Your profile already includes "
                f"{matched_text}, which aligns with "
                f"this role's requirements."
            )

        else:

            why_text = (
                "This role was selected based on "
                "similarity between your current skills "
                "and the job requirements."
            )


        # ----------------------------------------------------
        # Matched skills HTML
        # ----------------------------------------------------

        matched_html = ""

        for skill in matched:

            matched_html += f"""
            <span class="skill-good">
                ✓ {skill}
            </span>
            """


        # ----------------------------------------------------
        # Missing skills HTML
        # ----------------------------------------------------

        missing_html = ""

        for skill in missing:

            missing_html += f"""
            <span class="skill-missing">
                + {skill}
            </span>
            """


        render_html(
            f"""
            <div class="job-card">

                <div class="job-header">

                    <div>

                        <div class="job-title">
                            {job_title}
                        </div>

                        <div class="company">
                            {company}
                        </div>

                        <div class="location">
                            📍 {job_location}
                        </div>

                    </div>


                    <div class="match-box">

                        <div class="match-number">
                            {score:.1f}%
                        </div>

                        <div class="match-label">
                            MATCH
                        </div>

                    </div>

                </div>


                <div class="job-divider"></div>


                <div class="skill-heading">
                    SKILLS YOU ALREADY HAVE
                </div>

                <div class="skill-row">
                    {matched_html if matched_html else
                     '<span style="color:#8A94A5;font-size:10px;">No direct skill overlap detected</span>'}
                </div>


                {
                    f'''
                    <div style="margin-top:15px;">

                        <div class="skill-heading">
                            SKILLS TO STRENGTHEN
                        </div>

                        <div class="skill-row">
                            {missing_html}
                        </div>

                    </div>
                    '''
                    if missing_html else ""
                }


                <div class="why-box">

                    <div class="why-title">
                        WHY THIS MATCH?
                    </div>

                    <div class="why-text">
                        {why_text}
                    </div>

                </div>

            </div>
            """
        )


        # ----------------------------------------------------
# Job Details + External Opportunity
# ----------------------------------------------------

job_index = jobs.index(job)

if st.button(
    "View Job Details →",
    key=f"job_details_{job_index}",
    use_container_width=True
):

    st.session_state["selected_job"] = job

    st.switch_page(
        "pages/job_details.py"
    )


source_url = job.get(
    "source_url",
    ""
)

if source_url:

    st.link_button(
        "View Original Opportunity →",
        source_url,
        use_container_width=True
    )


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

render_html(
    """
    <div class="section">

        <div class="eyebrow">
            STEP 04
        </div>

        <div class="section-title">
            Skill gap analysis
        </div>

        <div class="section-text">
            Understand what you already bring to the table
            and which skills can improve your career alignment.
        </div>

    </div>
    """
)


# Collect missing skills from all jobs

all_missing = []

all_matched = []

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

    all_missing.extend(missing)
    all_matched.extend(matched)


missing_unique = list(
    dict.fromkeys(
        all_missing
    )
)

matched_unique = list(
    dict.fromkeys(
        all_matched
    )
)


total_skills = (
    len(matched_unique)
    +
    len(missing_unique)
)


if total_skills > 0:

    coverage = (
        len(matched_unique)
        /
        total_skills
    ) * 100

else:

    coverage = 0


gap_percentage = 100 - coverage


g1, g2, g3 = st.columns(
    3,
    gap="medium"
)


with g1:

    render_html(
        f"""
        <div class="gap-card">

            <div class="gap-stat">

                <div class="gap-stat-number">
                    {len(matched_unique)}
                </div>

                <div class="gap-stat-label">
                    MATCHED SKILLS
                </div>

            </div>

        </div>
        """
    )


with g2:

    render_html(
        f"""
        <div class="gap-card">

            <div class="gap-stat">

                <div class="gap-stat-number">
                    {len(missing_unique)}
                </div>

                <div class="gap-stat-label">
                    SKILLS TO BUILD
                </div>

            </div>

        </div>
        """
    )


with g3:

    render_html(
        f"""
        <div class="gap-card">

            <div class="gap-stat">

                <div class="gap-stat-number">
                    {coverage:.0f}%
                </div>

                <div class="gap-stat-label">
                    SKILL COVERAGE
                </div>

            </div>

        </div>
        """
    )


if missing_unique:

    st.write("")

    missing_html = ""

    for skill in missing_unique:

        missing_html += f"""
        <span class="skill-missing">
            + {skill}
        </span>
        """

    render_html(
        f"""
        <div class="gap-card">

            <div class="skill-heading">
                PRIORITY SKILLS TO DEVELOP
            </div>

            <div class="skill-row">
                {missing_html}
            </div>

            <div class="gap-progress">

                <div
                    class="gap-progress-fill"
                    style="width:{coverage:.0f}%"
                ></div>

            </div>

        </div>
        """
    )


# ============================================================
# LEARNING PATH
# ============================================================

render_html(
    """
    <div class="section">

        <div class="eyebrow">
            STEP 05
        </div>

        <div class="section-title">
            Recommended learning path
        </div>

        <div class="section-text">
            Courses selected around the skills identified
            in your career gap analysis.
        </div>

    </div>
    """
)


try:

    courses = recommend_courses(
        missing_unique,
        top_k=6
    )

except Exception:

    courses = []


if courses:

    course_columns = st.columns(
        3,
        gap="medium"
    )


    for index, course in enumerate(courses):

        column = course_columns[
            index % 3
        ]

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
            ""
        )

        url = course.get(
            "url",
            ""
        )


        with column:

            render_html(
                f"""
                <div class="course-card">

                    <div class="course-platform">
                        {platform.upper()}
                    </div>

                    <div class="course-title">
                        {course_name}
                    </div>

                    <div class="course-level">
                        {level}
                    </div>

                    <div class="course-duration">
                        {duration}
                    </div>

                </div>
                """
            )


            if url:

                st.link_button(
                    "Explore Course →",
                    url,
                    use_container_width=True
                )


else:

    render_html(
        """
        <div style="
            background:#FFFFFF;
            border:1px solid #E1E6EE;
            border-radius:14px;
            padding:28px;
            text-align:center;
        ">

            <div style="
                color:#56627A;
                font-size:12px;
                font-weight:750;
            ">
                No additional courses are required yet.
            </div>

            <div style="
                color:#8A94A5;
                font-size:10px;
                margin-top:5px;
            ">
                Add more target skills or explore different roles
                to generate additional recommendations.
            </div>

        </div>
        """
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

render_html(
    """
    <div style="
        background:linear-gradient(
            135deg,
            #0B1628,
            #1E355B
        );

        border-radius:20px;

        padding:35px;

        margin-top:55px;

        text-align:center;
    ">

        <div style="
            color:#FFFFFF;
            font-size:23px;
            font-weight:880;
        ">
            Your direction is becoming clearer.
        </div>

        <div style="
            color:#BFCBDD;
            font-size:11px;
            line-height:1.6;
            max-width:650px;
            margin:8px auto 0;
        ">
            Use your matched opportunities to understand
            where your current profile fits, then use the
            skill gaps and learning path to prepare for
            your target roles.
        </div>

    </div>
    """
)


# ============================================================
# BACK BUTTON
# ============================================================

st.write("")
st.write("")

back_col1, back_col2, back_col3 = st.columns(
    [1, 2, 1]
)

with back_col2:

    if st.button(
        "← Update My Profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/home.py"
        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        © Career Compass · Intelligent Career Navigation
    </div>
    """
)