import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Job Opportunities | Career Compass",
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


/* FILTER / SUMMARY */

.summary-card {
    background: #FFFFFF;

    border: 1px solid #E1E6EE;
    border-radius: 13px;

    padding: 18px 20px;

    margin-bottom: 25px;
}

.summary-label {
    color: #8993A5;

    font-size: 9px;
    font-weight: 850;

    letter-spacing: .7px;
}

.summary-value {
    color: #172033;

    font-size: 23px;
    font-weight: 900;

    margin-top: 5px;
}


/* JOB CARD */

.job-card {
    background: #FFFFFF;

    border: 1px solid #E1E6EE;
    border-radius: 15px;

    padding: 23px;

    margin-bottom: 18px;
}

.job-title {
    color: #172033;

    font-size: 18px;
    font-weight: 850;
}

.company {
    color: #526078;

    font-size: 12px;

    margin-top: 6px;
}

.location {
    color: #8A94A5;

    font-size: 10px;

    margin-top: 6px;
}

.match-label {
    color: #6B8B7B;

    font-size: 8px;
    font-weight: 850;

    letter-spacing: .6px;
}

.match {
    color: #16855A;

    font-size: 27px;
    font-weight: 900;

    margin-top: 3px;
}


/* SKILLS */

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


/* BUTTON */

div[data-testid="stButton"] > button {
    border-radius: 8px !important;

    min-height: 43px !important;

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
        JOB OPPORTUNITIES
    </div>

</div>
""")


# ============================================================
# GET ANALYSIS
# ============================================================

result = st.session_state.get(
    "career_result",
    None
)


if result is None:

    st.error(
        "Please complete your career analysis first."
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
# GET JOBS
# ============================================================

jobs = result.get(
    "jobs",
    []
)


profile = result.get(
    "profile",
    {}
)


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="eyebrow">
    OPPORTUNITY DISCOVERY
</div>

<div class="page-title">
    Job opportunities
</div>

<div class="page-description">
    Explore roles matched to your current skills,
    location and career interests.
</div>
""")


# ============================================================
# SUMMARY
# ============================================================

location = profile.get(
    "location",
    "Your preferred location"
)


col1, col2, col3 = st.columns(
    3,
    gap="medium"
)


with col1:

    st.html(f"""
    <div class="summary-card">

        <div class="summary-label">
            MATCHED OPPORTUNITIES
        </div>

        <div class="summary-value">
            {len(jobs)}
        </div>

    </div>
    """)


with col2:

    best_match = 0

    if jobs:

        best_match = max(
            float(
                job.get(
                    "match_score",
                    0
                )
            )
            for job in jobs
        )

    st.html(f"""
    <div class="summary-card">

        <div class="summary-label">
            BEST MATCH
        </div>

        <div class="summary-value">
            {best_match:.1f}%
        </div>

    </div>
    """)


with col3:

    st.html(f"""
    <div class="summary-card">

        <div class="summary-label">
            PREFERRED LOCATION
        </div>

        <div class="summary-value"
             style="font-size:17px;">
            {location}
        </div>

    </div>
    """)


# ============================================================
# JOB LIST
# ============================================================

st.html("""
<div style="
    color:#172033;
    font-size:21px;
    font-weight:850;
    margin-top:20px;
    margin-bottom:15px;
">
    Recommended roles
</div>
""")


if not jobs:

    st.html("""
    <div class="job-card">

        <div class="job-title">
            No matching jobs found
        </div>

        <div class="company">
            Try adding more technical skills
            to your profile.
        </div>

    </div>
    """)

else:

    for index, job in enumerate(jobs):

        job_title = job.get(
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

        matched_skills = job.get(
            "matched_skills",
            []
        )

        missing_skills = job.get(
            "missing_skills",
            []
        )


        # ----------------------------------------------------
        # CARD
        # ----------------------------------------------------

        st.html(f"""
        <div class="job-card">

            <div style="
                display:flex;
                justify-content:space-between;
                gap:30px;
            ">

                <div style="flex:1;">

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


                <div style="
                    text-align:right;
                    min-width:110px;
                ">

                    <div class="match-label">
                        MATCH SCORE
                    </div>

                    <div class="match">
                        {score:.1f}%
                    </div>

                </div>

            </div>


            <div style="
                margin-top:20px;
                padding-top:15px;
                border-top:1px solid #EEF1F5;
            ">

                <div style="
                    color:#8993A5;
                    font-size:8px;
                    font-weight:850;
                    letter-spacing:.7px;
                ">
                    MATCHED SKILLS
                </div>

                <div style="margin-top:4px;">

                    {
                        "".join(
                            f'<span class="skill">{skill}</span>'
                            for skill in matched_skills
                        )
                        if matched_skills
                        else '<span style="color:#8993A5;font-size:9px;">No direct matches</span>'
                    }

                </div>

            </div>


            <div style="margin-top:12px;">

                <div style="
                    color:#8993A5;
                    font-size:8px;
                    font-weight:850;
                    letter-spacing:.7px;
                ">
                    SKILLS TO DEVELOP
                </div>

                <div style="margin-top:4px;">

                    {
                        "".join(
                            f'<span class="missing-skill">{skill}</span>'
                            for skill in missing_skills[:8]
                        )
                        if missing_skills
                        else '<span style="color:#16855A;font-size:9px;">No major skill gaps</span>'
                    }

                </div>

            </div>

        </div>
        """)


        # ----------------------------------------------------
        # VIEW DETAILS BUTTON
        # ----------------------------------------------------

        if st.button(
            "View job details →",
            key=f"job_details_{index}",
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
# BACK
# ============================================================

if st.button(
    "← Back to Career Analysis",
    use_container_width=True
):

    st.switch_page(
        "pages/analysis.py"
    )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    © Career Compass · Intelligent Career Navigation
</div>
""")