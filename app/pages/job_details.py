import streamlit as st
import textwrap


# ============================================================
# HTML HELPER
# ============================================================

def render_html(html):
    st.html(textwrap.dedent(html).strip())


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Job Details | Career Compass",
    page_icon="🧭",
    layout="wide"
)


# ============================================================
# PROFESSIONAL DESIGN
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #F7F9FC;
    }

    .main .block-container {
        max-width: 1100px;
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

    .eyebrow {
        color: #356AE6;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 1.6px;
        margin-bottom: 8px;
    }

    .job-title {
        color: #101A2B;
        font-size: 36px;
        font-weight: 900;
        letter-spacing: -1.2px;
    }

    .company {
        color: #536078;
        font-size: 16px;
        font-weight: 700;
        margin-top: 8px;
    }

    .location {
        color: #7B8699;
        font-size: 12px;
        margin-top: 7px;
    }

    .hero-card {
        background: #FFFFFF;
        border: 1px solid #E1E6EE;
        border-radius: 18px;
        padding: 30px;
        box-shadow: 0 8px 28px rgba(25, 40, 65, 0.04);
        margin-bottom: 28px;
    }

    .stat-card {
        background: #FFFFFF;
        border: 1px solid #E1E6EE;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        min-height: 105px;
    }

    .stat-number {
        color: #16855A;
        font-size: 25px;
        font-weight: 900;
    }

    .stat-label {
        color: #8A94A5;
        font-size: 9px;
        font-weight: 850;
        letter-spacing: 0.7px;
        margin-top: 5px;
    }

    .content-card {
        background: #FFFFFF;
        border: 1px solid #E1E6EE;
        border-radius: 16px;
        padding: 25px;
        margin-top: 22px;
        box-shadow: 0 7px 22px rgba(25, 40, 65, 0.035);
    }

    .section-title {
        color: #182338;
        font-size: 17px;
        font-weight: 850;
        margin-bottom: 15px;
    }

    .section-text {
        color: #667188;
        font-size: 12px;
        line-height: 1.7;
    }

    .skill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 7px;
    }

    .skill-good {
        display: inline-block;
        background: #EEF8F3;
        color: #16855A;
        border: 1px solid #D6EDE1;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 9px;
        font-weight: 750;
    }

    .skill-missing {
        display: inline-block;
        background: #FFF7EC;
        color: #B76A17;
        border: 1px solid #F2DFC2;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 9px;
        font-weight: 750;
    }

    .gap-box {
        background: #FFF7EC;
        border: 1px solid #F2DFC2;
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
    }

    .gap-title {
        color: #B76A17;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.6px;
    }

    .gap-text {
        color: #806342;
        font-size: 11px;
        margin-top: 5px;
        line-height: 1.6;
    }

    div[data-testid="stButton"] > button {
        border-radius: 8px !important;
        min-height: 44px !important;
        font-weight: 800 !important;
    }

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
            JOB DETAILS
        </div>

    </div>
    """
)


# ============================================================
# GET SELECTED JOB
# ============================================================

job = st.session_state.get(
    "selected_job"
)


if not job:

    render_html(
        """
        <div class="content-card"
             style="text-align:center;padding:50px;">

            <div class="section-title">
                No job selected
            </div>

            <div class="section-text">
                Please return to your career analysis and
                select a job opportunity.
            </div>

        </div>
        """
    )

    if st.button(
        "← Back to Career Analysis",
        use_container_width=True
    ):
        st.switch_page(
    "pages/analysis.py"
)

    st.stop()


# ============================================================
# GET JOB DATA
# ============================================================

job_title = job.get(
    "job_title",
    "Untitled Role"
)

company = job.get(
    "company",
    "Company"
)

location = job.get(
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

gap_percentage = float(
    job.get(
        "gap_percentage",
        0
    )
)


# ============================================================
# CONVERT SKILLS TO LIST
# ============================================================

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


# ============================================================
# HERO
# ============================================================

render_html(
    f"""
    <div class="hero-card">

        <div class="eyebrow">
            SELECTED OPPORTUNITY
        </div>

        <div class="job-title">
            {job_title}
        </div>

        <div class="company">
            {company}
        </div>

        <div class="location">
            📍 {location}
        </div>

    </div>
    """
)


# ============================================================
# MATCH STATISTICS
# ============================================================

c1, c2, c3 = st.columns(
    3,
    gap="medium"
)


with c1:

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-number">
                {score:.1f}%
            </div>

            <div class="stat-label">
                PROFILE MATCH
            </div>

        </div>
        """
    )


with c2:

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-number">
                {len(matched)}
            </div>

            <div class="stat-label">
                MATCHED SKILLS
            </div>

        </div>
        """
    )


with c3:

    render_html(
        f"""
        <div class="stat-card">

            <div class="stat-number"
                 style="color:#B76A17;">
                {gap_percentage:.1f}%
            </div>

            <div class="stat-label">
                SKILL GAP
            </div>

        </div>
        """
    )


# ============================================================
# MATCHED SKILLS
# ============================================================

if matched:

    matched_html = ""

    for skill in matched:

        matched_html += f"""
        <span class="skill-good">
            ✓ {skill}
        </span>
        """

    render_html(
        f"""
        <div class="content-card">

            <div class="section-title">
                Skills you already have
            </div>

            <div class="section-text"
                 style="margin-bottom:15px;">
                These skills from your profile align with
                the requirements of this role.
            </div>

            <div class="skill-row">
                {matched_html}
            </div>

        </div>
        """
    )


# ============================================================
# MISSING SKILLS
# ============================================================

if missing:

    missing_html = ""

    for skill in missing:

        missing_html += f"""
        <span class="skill-missing">
            + {skill}
        </span>
        """

    render_html(
        f"""
        <div class="content-card">

            <div class="section-title">
                Skills to strengthen
            </div>

            <div class="section-text"
                 style="margin-bottom:15px;">
                These are the main areas you can develop
                to improve your alignment with this role.
            </div>

            <div class="skill-row">
                {missing_html}
            </div>

            <div class="gap-box">

                <div class="gap-title">
                    CAREER DEVELOPMENT AREA
                </div>

                <div class="gap-text">
                    Focus your learning on the missing skills
                    above and use the recommended learning
                    path from your career analysis.
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# LOCATION
# ============================================================

render_html(
    f"""
    <div class="content-card">

        <div class="section-title">
            Opportunity information
        </div>

        <div class="section-text">
            <strong>Company:</strong> {company}
            <br><br>
            <strong>Location:</strong> {location}
            <br><br>
            <strong>Profile alignment:</strong>
            Your current profile has a {score:.1f}%
            similarity match with this opportunity.
        </div>

    </div>
    """
)


# ============================================================
# ACTIONS
# ============================================================

st.write("")
st.write("")

a1, a2, a3 = st.columns(
    [1, 1.4, 1]
)


with a1:

    if st.button(
        "← Back to Career Analysis",
        use_container_width=True
    ):

        st.switch_page(
    "pages/analysis.py"
)

with a2:

    source_url = job.get(
        "source_url",
        ""
    )

    if source_url:

        st.link_button(
            "Open Original Opportunity →",
            source_url,
            use_container_width=True
        )
        st.write("")
st.write("")

if st.button(
    "Analyze Skill Gap →",
    type="primary",
    use_container_width=True
):

    st.switch_page(
        "pages/skill_gaps.py"
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