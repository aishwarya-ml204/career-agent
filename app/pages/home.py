import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Career Compass",
    page_icon="🧭",
    layout="wide"
)


# ============================================================
# CSS + HTML
# ============================================================

st.html("""
<style>

.stApp {
    background: #F7F9FC;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 0.5rem;
    padding-bottom: 3rem;
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
    margin-bottom: 35px;
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
    padding: 9px 14px;
    border-radius: 8px;
    font-size: 10px;
    font-weight: 850;
}


/* WELCOME */

.welcome {
    color: #101A2B;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: -1px;
}

.welcome-text {
    color: #748096;
    font-size: 13px;
    margin-top: 7px;
    line-height: 1.6;
}


/* STAT CARDS */

.stat-card {
    background: #FFFFFF;
    border: 1px solid #E1E6EE;
    border-radius: 13px;
    padding: 20px;
    min-height: 105px;
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
    margin-top: 3px;
}


/* SECTION */

.section-title {
    color: #172033;
    font-size: 21px;
    font-weight: 850;
    margin-top: 38px;
    margin-bottom: 12px;
}


/* PROFILE */

.profile-card {
    background: #FFFFFF;
    border: 1px solid #E1E6EE;
    border-radius: 15px;
    padding: 24px;
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


/* ACTION */

.action-card {
    background: #0B1628;
    border-radius: 15px;
    padding: 25px;
}

.action-title {
    color: #FFFFFF;
    font-size: 19px;
    font-weight: 850;
}

.action-text {
    color: #BFCBDD;
    font-size: 11px;
    line-height: 1.6;
    margin-top: 7px;
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
        CAREER DASHBOARD
    </div>

</div>
""")


# ============================================================
# SESSION DATA
# ============================================================

profile = st.session_state.get(
    "profile_input",
    {}
)

result = st.session_state.get(
    "career_result"
)

education = profile.get(
    "education",
    "Not completed"
)

location = profile.get(
    "location",
    "Not specified"
)

skills = profile.get(
    "skills",
    "Add your skills"
)

interests = profile.get(
    "interests",
    "Add your interests"
)

jobs = []

if result:
    jobs = result.get(
        "jobs",
        []
    )


# ============================================================
# PROFILE COMPLETION
# ============================================================

if profile:

    completed = sum(
        bool(profile.get(key))
        for key in [
            "education",
            "location",
            "skills",
            "interests"
        ]
    )

    profile_score = int(
        completed / 4 * 100
    )

else:

    profile_score = 0


# ============================================================
# WELCOME
# ============================================================

st.html("""
<div class="welcome">
    Welcome to your career dashboard
</div>

<div class="welcome-text">
    Track your profile, discover relevant opportunities,
    understand your skill gaps and follow your personalized
    learning direction.
</div>
""")


st.write("")


# ============================================================
# STATISTICS
# ============================================================

c1, c2, c3, c4 = st.columns(
    4,
    gap="medium"
)


with c1:

    st.html(f"""
    <div class="stat-card">

        <div class="stat-label">
            PROFILE COMPLETION
        </div>

        <div class="stat-number">
            {profile_score}%
        </div>

        <div class="stat-small">
            Your profile strength
        </div>

    </div>
    """)


with c2:

    st.html(f"""
    <div class="stat-card">

        <div class="stat-label">
            JOB MATCHES
        </div>

        <div class="stat-number">
            {len(jobs)}
        </div>

        <div class="stat-small">
            AI-matched opportunities
        </div>

    </div>
    """)


with c3:

    skill_count = 0

    if skills and skills != "Add your skills":

        skill_count = len([
            x for x in skills.split(",")
            if x.strip()
        ])

    st.html(f"""
    <div class="stat-card">

        <div class="stat-label">
            SKILLS TRACKED
        </div>

        <div class="stat-number">
            {skill_count}
        </div>

        <div class="stat-small">
            Skills in your profile
        </div>

    </div>
    """)


with c4:

    status = "Ready" if result else "Start"

    st.html(f"""
    <div class="stat-card">

        <div class="stat-label">
            CAREER STATUS
        </div>

        <div class="stat-number">
            {status}
        </div>

        <div class="stat-small">
            Continue building
        </div>

    </div>
    """)


# ============================================================
# CAREER SNAPSHOT
# ============================================================

st.html("""
<div class="section-title">
    Your career snapshot
</div>
""")


st.html(f"""
<div class="profile-card">

    <div style="
        display:grid;
        grid-template-columns:repeat(2,1fr);
        gap:22px;
    ">

        <div>

            <div class="profile-label">
                EDUCATION
            </div>

            <div class="profile-value">
                {education}
            </div>

        </div>


        <div>

            <div class="profile-label">
                LOCATION
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
                {interests}
            </div>

        </div>

    </div>

</div>
""")


# ============================================================
# ACTIONS
# ============================================================

st.html("""
<div class="section-title">
    Continue your career journey
</div>
""")


a1, a2 = st.columns(
    2,
    gap="medium"
)


with a1:

    st.html("""
    <div class="action-card">

        <div class="action-title">
            Build or update your profile
        </div>

        <div class="action-text">
            Add your education, skills, interests and
            preferred location to generate better
            career recommendations.
        </div>

    </div>
    """)

    if st.button(
        "Open Profile →",
        use_container_width=True
    ):

        st.switch_page(
            "pages/profile.py"
        )


with a2:

    st.html("""
    <div class="action-card">

        <div class="action-title">
            Explore your career analysis
        </div>

        <div class="action-text">
            Review AI-powered job matches, skill gaps
            and your personalized development path.
        </div>

    </div>
    """)

    if st.button(
        "View Career Analysis →",
        use_container_width=True
    ):

        if result:

            st.switch_page(
                "pages/analysis.py"
            )

        else:

            st.switch_page(
                "pages/profile.py"
            )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    © Career Compass · Intelligent Career Navigation
</div>
""")