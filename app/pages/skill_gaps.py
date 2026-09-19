import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Skill Gap Analysis | Career Compass",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.html("""
<style>

.stApp {
    background: #F7F9FC;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 0.5rem;
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


/* TOP BAR */

.topbar {
    height: 68px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-bottom: 1px solid #E1E6EE;

    margin-bottom: 38px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 42px;
    height: 42px;

    background: #0B1628;
    border-radius: 10px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 19px;
}

.brand-name {
    font-size: 19px;
    font-weight: 850;
    color: #101A2B;
}

.brand-sub {
    font-size: 8px;
    color: #8791A2;
    letter-spacing: 1px;
    margin-top: 3px;
}

.page-label {
    background: #EEF3FF;
    color: #356AE6;

    padding: 10px 15px;
    border-radius: 8px;

    font-size: 10px;
    font-weight: 850;
}


/* HEADER */

.eyebrow {
    color: #356AE6;

    font-size: 10px;
    font-weight: 900;

    letter-spacing: 1.7px;
}

.page-title {
    color: #101A2B;

    font-size: 36px;
    font-weight: 900;

    letter-spacing: -1.2px;

    margin-top: 8px;
}

.page-description {
    color: #748096;

    font-size: 13px;
    line-height: 1.7;

    max-width: 760px;

    margin-top: 8px;
    margin-bottom: 30px;
}


/* JOB CARD */

.job-card {
    background: #FFFFFF;

    border: 1px solid #E1E6EE;
    border-radius: 15px;

    padding: 23px;

    margin-bottom: 25px;
}

.job-title {
    color: #172033;

    font-size: 20px;
    font-weight: 850;
}

.company {
    color: #687489;

    font-size: 12px;

    margin-top: 6px;
}


/* GAP CARD */

.gap-card {
    background: #FFFFFF;

    border: 1px solid #E1E6EE;
    border-radius: 15px;

    padding: 25px;

    margin-top: 20px;
}

.gap-number {
    color: #C27619;

    font-size: 32px;
    font-weight: 900;
}

.gap-label {
    color: #8993A5;

    font-size: 9px;
    font-weight: 850;

    letter-spacing: .7px;
}


/* SKILLS */

.skill-match {
    display: inline-block;

    background: #EEF8F3;
    color: #16855A;

    border: 1px solid #D6EDE1;

    padding: 7px 10px;

    border-radius: 7px;

    font-size: 10px;
    font-weight: 700;

    margin: 4px 4px 0 0;
}

.skill-missing {
    display: inline-block;

    background: #FFF5EA;
    color: #B76A18;

    border: 1px solid #F0DEC5;

    padding: 7px 10px;

    border-radius: 7px;

    font-size: 10px;
    font-weight: 700;

    margin: 4px 4px 0 0;
}


/* EXPLANATION */

.insight-card {
    background: #0B1628;

    border-radius: 15px;

    padding: 25px;

    margin-top: 25px;
}

.insight-title {
    color: #FFFFFF;

    font-size: 19px;
    font-weight: 850;
}

.insight-text {
    color: #BFCBDD;

    font-size: 11px;
    line-height: 1.8;

    margin-top: 8px;
}


/* BUTTON */

div[data-testid="stButton"] > button {
    border-radius: 8px !important;
    min-height: 44px !important;
    font-weight: 800 !important;
}


/* FOOTER */

.footer {
    text-align: center;

    color: #929CAD;

    font-size: 9px;

    margin-top: 55px;
    padding-top: 25px;

    border-top: 1px solid #E1E6EE;
}

</style>
""")


# ============================================================
# TOP BAR
# ============================================================

st.html("""
<div class="topbar">

    <div class="brand">

        <div class="brand-icon">
            🧭
        </div>

        <div>

            <div class="brand-name">
                Career Compass
            </div>

            <div class="brand-sub">
                INTELLIGENT CAREER NAVIGATION
            </div>

        </div>

    </div>

    <div class="page-label">
        SKILL GAP ANALYSIS
    </div>

</div>
""")


# ============================================================
# GET SELECTED JOB
# ============================================================

job = st.session_state.get(
    "selected_job",
    None
)


# ============================================================
# SAFETY CHECK
# ============================================================

if job is None:

    st.error(
        "Please select a job opportunity first."
    )

    if st.button(
        "← Explore Job Opportunities",
        use_container_width=True
    ):

        st.switch_page(
            "pages/jobs.py"
        )

    st.stop()


# ============================================================
# JOB INFORMATION
# ============================================================

job_title = job.get(
    "job_title",
    "Selected Role"
)

company = job.get(
    "company",
    "Company"
)

location = job.get(
    "location",
    "Location"
)

match_score = float(
    job.get(
        "match_score",
        0
    )
)

gap_percentage = float(
    job.get(
        "gap_percentage",
        0
    )
)

matched_skills = job.get(
    "matched_skills",
    []
)

missing_skills = job.get(
    "missing_skills",
    []
)


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="eyebrow">
    CAPABILITY ASSESSMENT
</div>

<div class="page-title">
    Understand your skill gap
</div>

<div class="page-description">
    Career Compass compares your current capabilities
    with the requirements of your selected role and
    identifies the skills you can strengthen next.
</div>
""")


# ============================================================
# SELECTED ROLE
# ============================================================

st.html(f"""
<div class="job-card">

    <div class="job-title">
        {job_title}
    </div>

    <div class="company">
        {company} · 📍 {location}
    </div>

</div>
""")


# ============================================================
# SUMMARY
# ============================================================

col1, col2, col3 = st.columns(
    3,
    gap="medium"
)


with col1:

    st.html(f"""
    <div class="gap-card">

        <div class="gap-label">
            PROFILE MATCH
        </div>

        <div class="gap-number"
             style="color:#16855A;">
            {match_score:.1f}%
        </div>

    </div>
    """)


with col2:

    st.html(f"""
    <div class="gap-card">

        <div class="gap-label">
            SKILLS YOU HAVE
        </div>

        <div class="gap-number"
             style="color:#16855A;">
            {len(matched_skills)}
        </div>

    </div>
    """)


with col3:

    st.html(f"""
    <div class="gap-card">

        <div class="gap-label">
            SKILL GAP
        </div>

        <div class="gap-number">
            {gap_percentage:.1f}%
        </div>

    </div>
    """)


# ============================================================
# SKILLS YOU HAVE
# ============================================================

st.html("""
<div style="
    color:#172033;
    font-size:21px;
    font-weight:850;
    margin-top:40px;
    margin-bottom:12px;
">
    Skills you already have
</div>
""")


if matched_skills:

    matched_html = "".join(
        f'<span class="skill-match">✓ {skill}</span>'
        for skill in matched_skills
    )

    st.html(f"""
    <div class="gap-card">

        <div style="
            color:#748096;
            font-size:12px;
            margin-bottom:10px;
        ">
            These skills already align with the
            requirements of this role.
        </div>

        {matched_html}

    </div>
    """)

else:

    st.html("""
    <div class="gap-card">

        <div style="
            color:#748096;
            font-size:12px;
        ">
            No direct skill matches were identified
            for this role.
        </div>

    </div>
    """)


# ============================================================
# SKILLS TO STRENGTHEN
# ============================================================

st.html("""
<div style="
    color:#172033;
    font-size:21px;
    font-weight:850;
    margin-top:40px;
    margin-bottom:12px;
">
    Skills to strengthen
</div>
""")


if missing_skills:

    missing_html = "".join(
        f'<span class="skill-missing">+ {skill}</span>'
        for skill in missing_skills
    )

    st.html(f"""
    <div class="gap-card">

        <div style="
            color:#748096;
            font-size:12px;
            margin-bottom:10px;
        ">
            These capabilities are currently missing
            from your profile for this role.
        </div>

        {missing_html}

    </div>
    """)

else:

    st.html("""
    <div class="gap-card">

        <div style="
            color:#16855A;
            font-size:13px;
            font-weight:700;
        ">
            ✓ No major skill gaps identified.
        </div>

    </div>
    """)


# ============================================================
# INSIGHT
# ============================================================

if missing_skills:

    skills_text = ", ".join(
        missing_skills[:8]
    )

    st.html(f"""
    <div class="insight-card">

        <div class="insight-title">
            Your development focus
        </div>

        <div class="insight-text">
            To improve your alignment with
            <strong>{job_title}</strong> at
            <strong>{company}</strong>, focus on
            strengthening:
            <strong>{skills_text}</strong>.
            Career Compass will use these skill gaps
            to generate your personalized learning path.
        </div>

    </div>
    """)


# ============================================================
# CONTINUE TO LEARNING
# ============================================================

st.write("")
st.write("")

if st.button(
    "Build my personalized learning path →",
    type="primary",
    use_container_width=True
):

    st.switch_page(
        "pages/learning_path.py"
    )


# ============================================================
# BACK
# ============================================================

if st.button(
    "← Back to Job Details",
    use_container_width=True
):

    st.switch_page(
        "pages/job_details.py"
    )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    © Career Compass · Intelligent Career Navigation
</div>
""")