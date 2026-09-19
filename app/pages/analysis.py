import streamlit as st

from agents.career_pipeline import run_career_analysis


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Career Analysis | Career Compass",
    page_icon="🧭",
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


/* ==========================================================
   TOP BAR
   ========================================================== */

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

    color: white;
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


/* ==========================================================
   HEADER
   ========================================================== */

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


/* ==========================================================
   STAT CARDS
   ========================================================== */

.stat-card {
    background: #FFFFFF;

    border: 1px solid #E1E6EE;
    border-radius: 13px;

    padding: 20px;

    min-height: 112px;
}

.stat-label {
    color: #8993A5;

    font-size: 9px;
    font-weight: 850;

    letter-spacing: .7px;
}

.stat-number {
    color: #172033;

    font-size: 26px;
    font-weight: 900;

    margin-top: 7px;
}

.stat-small {
    color: #6F7B8F;

    font-size: 9px;

    margin-top: 4px;
}


/* ==========================================================
   SECTION
   ========================================================== */

.section-title {
    color: #172033;

    font-size: 21px;
    font-weight: 850;

    margin-top: 38px;
    margin-bottom: 13px;
}


/* ==========================================================
   PROFILE CARD
   ========================================================== */

.profile-card {
    background: #FFFFFF;

    border: 1px solid #E1E6EE;
    border-radius: 15px;

    padding: 22px;
}

.profile-label {
    color: #8A94A5;

    font-size: 8px;
    font-weight: 900;

    letter-spacing: .8px;
}

.profile-value {
    color: #263248;

    font-size: 12px;
    font-weight: 700;

    margin-top: 5px;
}


/* ==========================================================
   JOB CARD
   ========================================================== */

.job-card {
    background: #FFFFFF;

    border: 1px solid #E1E6EE;
    border-radius: 14px;

    padding: 20px;

    min-height: 170px;
}

.job-title {
    color: #172033;

    font-size: 15px;
    font-weight: 850;
}

.company {
    color: #687489;

    font-size: 11px;

    margin-top: 5px;
}

.location {
    color: #8A94A5;

    font-size: 9px;

    margin-top: 5px;
}

.match {
    color: #16855A;

    font-size: 22px;
    font-weight: 900;
}

.match-label {
    color: #6B8B7B;

    font-size: 8px;
    font-weight: 800;
}

.skill {
    display: inline-block;

    background: #EEF8F3;
    color: #16855A;

    border: 1px solid #D6EDE1;

    padding: 5px 8px;

    border-radius: 6px;

    font-size: 8px;

    margin: 3px 3px 0 0;
}

.missing-skill {
    display: inline-block;

    background: #FFF5EA;
    color: #B76A18;

    border: 1px solid #F0DEC5;

    padding: 5px 8px;

    border-radius: 6px;

    font-size: 8px;

    margin: 3px 3px 0 0;
}


/* ==========================================================
   INFO CARD
   ========================================================== */

.info-card {
    background: #0B1628;

    border-radius: 15px;

    padding: 25px;
}

.info-title {
    color: #FFFFFF;

    font-size: 19px;
    font-weight: 850;
}

.info-text {
    color: #BFCBDD;

    font-size: 11px;
    line-height: 1.7;

    margin-top: 7px;
}


/* ==========================================================
   BUTTON
   ========================================================== */

div[data-testid="stButton"] > button {
    border-radius: 8px !important;

    min-height: 44px !important;

    font-weight: 800 !important;
}


/* ==========================================================
   FOOTER
   ========================================================== */

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
        AI CAREER ANALYSIS
    </div>

</div>
""")


# ============================================================
# GET PROFILE
# ============================================================

profile = st.session_state.get(
    "profile_input",
    {}
)


# ============================================================
# GET EXISTING ANALYSIS
# ============================================================

result = st.session_state.get(
    "career_result",
    None
)


# ============================================================
# RECOVER ANALYSIS IF NEEDED
# ============================================================

if result is None and profile:

    education = profile.get(
        "education",
        ""
    )

    location = profile.get(
        "location",
        ""
    )

    skills = profile.get(
        "skills",
        ""
    )

    interests = profile.get(
        "interests",
        ""
    )

    profile_text = f"""
I am a {education}.
I live in {location}.
I know {skills}.
I am interested in {interests}.
"""

    with st.spinner(
        "Preparing your AI career analysis..."
    ):

        try:

            result = run_career_analysis(
                profile_text,
                top_k=5
            )

            st.session_state[
                "career_result"
            ] = result

            st.session_state[
                "analysis_ready"
            ] = True

        except Exception as e:

            st.error(
                f"Unable to prepare your analysis: {e}"
            )

            st.stop()


# ============================================================
# PROFILE NOT AVAILABLE
# ============================================================

if not profile:

    st.error(
        "Please complete your career profile first."
    )

    if st.button(
        "← Build My Profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/profile.py"
        )

    st.stop()


# ============================================================
# SAFETY CHECK
# ============================================================

if result is None:

    st.error(
        "Your career analysis could not be generated."
    )

    if st.button(
        "← Build My Profile",
        use_container_width=True
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
# PROFILE VALUES
# ============================================================

education = profile.get(
    "education",
    "Not specified"
)

location = profile.get(
    "location",
    "Not specified"
)

skills = profile.get(
    "skills",
    "Not specified"
)

interests = profile.get(
    "interests",
    "Not specified"
)


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="eyebrow">
    AI-POWERED INSIGHT
</div>

<div class="page-title">
    Your career analysis
</div>

<div class="page-description">
    Career Compass has analyzed your profile against
    available opportunities and identified where your
    current capabilities align.
</div>
""")


st.write("")


# ============================================================
# SUMMARY STATISTICS
# ============================================================

job_count = len(jobs)

if job_count > 0:

    best_match = max(
        float(
            job.get(
                "match_score",
                0
            )
        )
        for job in jobs
    )

else:

    best_match = 0


skill_list = [
    skill.strip()
    for skill in skills.split(",")
    if skill.strip()
]


col1, col2, col3, col4 = st.columns(
    4,
    gap="medium"
)


with col1:

    st.html(f"""
    <div class="stat-card">

        <div class="stat-label">
            JOB OPPORTUNITIES
        </div>

        <div class="stat-number">
            {job_count}
        </div>

        <div class="stat-small">
            AI-matched roles
        </div>

    </div>
    """)


with col2:

    st.html(f"""
    <div class="stat-card">

        <div class="stat-label">
            BEST MATCH
        </div>

        <div class="stat-number">
            {best_match:.1f}%
        </div>

        <div class="stat-small">
            Highest compatibility
        </div>

    </div>
    """)


with col3:

    st.html(f"""
    <div class="stat-card">

        <div class="stat-label">
            CURRENT SKILLS
        </div>

        <div class="stat-number">
            {len(skill_list)}
        </div>

        <div class="stat-small">
            Skills in your profile
        </div>

    </div>
    """)


with col4:

    st.html("""
    <div class="stat-card">

        <div class="stat-label">
            ANALYSIS STATUS
        </div>

        <div class="stat-number">
            Ready
        </div>

        <div class="stat-small">
            Profile successfully analyzed
        </div>

    </div>
    """)


# ============================================================
# PROFILE SNAPSHOT
# ============================================================

st.html("""
<div class="section-title">
    Profile snapshot
</div>
""")


st.html(f"""
<div class="profile-card">

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:22px;">

        <div>

            <div class="profile-label">
                ACADEMIC BACKGROUND
            </div>

            <div class="profile-value">
                {education}
            </div>

        </div>


        <div>

            <div class="profile-label">
                PREFERRED LOCATION
            </div>

            <div class="profile-value">
                {location}
            </div>

        </div>


        <div>

            <div class="profile-label">
                TECHNICAL SKILLS
            </div>

            <div class="profile-value">
                {skills}
            </div>

        </div>


        <div>

            <div class="profile-label">
                CAREER INTERESTS
            </div>

            <div class="profile-value">
                {interests if interests else "Not specified"}
            </div>

        </div>

    </div>

</div>
""")


# ============================================================
# JOB OPPORTUNITIES PREVIEW
# ============================================================

st.html("""
<div class="section-title">
    Recommended opportunities
</div>
""")


if not jobs:

    st.html("""
    <div class="profile-card">

        <div class="page-title"
             style="font-size:20px;">
            No matching opportunities found
        </div>

        <div class="page-description"
             style="margin-bottom:0;">
            We couldn't find roles matching your
            selected location and skills.
            Try updating your profile with additional
            skills or another preferred location.
        </div>

    </div>
    """)

else:

    # Show the first 3 jobs as a preview
    preview_jobs = jobs[:3]

    for index, job in enumerate(preview_jobs):

        title = job.get(
            "job_title",
            "Untitled role"
        )

        company = job.get(
            "company",
            "Company not specified"
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


        left, right = st.columns(
            [4, 1],
            gap="medium"
        )


        with left:

            matched_html = ""

            for skill in matched[:5]:

                matched_html += (
                    f'<span class="skill">'
                    f'{skill}'
                    f'</span>'
                )


            missing_html = ""

            for skill in missing[:5]:

                missing_html += (
                    f'<span class="missing-skill">'
                    f'{skill}'
                    f'</span>'
                )


            st.html(f"""
            <div class="job-card">

                <div class="job-title">
                    {title}
                </div>

                <div class="company">
                    {company}
                </div>

                <div class="location">
                    📍 {job_location}
                </div>

                <div style="margin-top:14px;">

                    <div class="match-label">
                        MATCH SCORE
                    </div>

                    <div class="match">
                        {score:.1f}%
                    </div>

                </div>

                <div style="margin-top:10px;">

                    <div class="profile-label">
                        MATCHED SKILLS
                    </div>

                    {matched_html if matched_html else
                     '<span class="stat-small">None yet</span>'}

                </div>

                <div style="margin-top:8px;">

                    <div class="profile-label">
                        SKILLS TO DEVELOP
                    </div>

                    {missing_html if missing_html else
                     '<span class="stat-small">No major gaps</span>'}

                </div>

            </div>
            """)


        with right:

            st.write("")

            st.write("")

            if st.button(
                "View details →",
                key=f"analysis_job_{index}",
                use_container_width=True
            ):

                st.session_state[
                    "selected_job"
                ] = job

                st.switch_page(
                    "pages/job_details.py"
                )


        st.write("")


# ============================================================
# INSIGHT
# ============================================================

if jobs:

    missing_all = []

    for job in jobs:

        missing_all.extend(
            job.get(
                "missing_skills",
                []
            )
        )


    unique_missing = []

    for skill in missing_all:

        if skill not in unique_missing:

            unique_missing.append(skill)


    missing_preview = ", ".join(
        unique_missing[:6]
    )

    if missing_preview:

        st.html(f"""
        <div class="info-card">

            <div class="info-title">
                Your next career move
            </div>

            <div class="info-text">
                Your current profile already matches
                several available opportunities.
                Across the recommended roles, the main
                skills to strengthen include:
                <strong>{missing_preview}</strong>.
                These gaps will be used to build your
                personalized learning path.
            </div>

        </div>
        """)


# ============================================================
# CONTINUE BUTTON
# ============================================================

st.write("")
st.write("")


if jobs:

    if st.button(
        "Explore all job opportunities →",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/jobs.py"
        )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    © Career Compass · Intelligent Career Navigation
</div>
""")