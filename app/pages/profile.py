import streamlit as st

from agents.career_pipeline import run_career_analysis


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Build Profile | Career Compass",
    page_icon="🧭",
    layout="wide"
)


# ============================================================
# DESIGN
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
    margin-top: 7px;
    margin-bottom: 30px;
}


/* FORM */

.form-card {
    background: #FFFFFF;
    border: 1px solid #E1E6EE;
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 22px;
}

.form-heading {
    color: #172033;
    font-size: 19px;
    font-weight: 850;
}

.form-sub {
    color: #7A8598;
    font-size: 11px;
    margin-top: 5px;
    line-height: 1.6;
}


/* BUTTON */

div[data-testid="stButton"] > button {
    border-radius: 8px !important;
    min-height: 45px !important;
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
        BUILD YOUR PROFILE
    </div>

</div>
""")


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="eyebrow">
    PERSONALIZED ANALYSIS
</div>

<div class="page-title">
    Build your career profile
</div>

<div class="page-description">
    Tell Career Compass where you are today.
    We will determine where you can go next.
</div>
""")


# ============================================================
# FORM INTRO
# ============================================================

st.html("""
<div class="form-card">

    <div class="form-heading">
        Your information
    </div>

    <div class="form-sub">
        The more accurate your profile, the more relevant
        your career matches will be.
    </div>

</div>
""")


# ============================================================
# FORM
# ============================================================

col1, col2 = st.columns(
    2,
    gap="medium"
)


with col1:

    education = st.text_input(
        "Academic background",
        placeholder="e.g. B.Tech Computer Science"
    )


with col2:

    location = st.text_input(
        "Preferred location",
        placeholder="e.g. Bengaluru, Karnataka"
    )


col3, col4 = st.columns(
    2,
    gap="medium"
)


with col3:

    skills = st.text_area(
        "Technical skills",
        placeholder="e.g. Python, SQL, Java, Pandas, Git",
        height=130
    )


with col4:

    interests = st.text_area(
        "Career interests",
        placeholder="e.g. Data Science, AI, Software Development",
        height=130
    )


st.write("")
st.write("")


# ============================================================
# ANALYZE
# ============================================================

if st.button(
    "Analyze my career →",
    type="primary",
    use_container_width=False
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not education.strip():

        st.error(
            "Please enter your academic background."
        )

        st.stop()


    if not location.strip():

        st.error(
            "Please enter your preferred location."
        )

        st.stop()


    if not skills.strip():

        st.error(
            "Please enter your technical skills."
        )

        st.stop()


    # --------------------------------------------------------
    # PROFILE TEXT
    # --------------------------------------------------------

    profile_text = f"""
I am a {education}.
I live in {location}.
I know {skills}.
I am interested in {interests}.
"""


    # --------------------------------------------------------
    # SAVE PROFILE FIRST
    # --------------------------------------------------------

    st.session_state["profile_input"] = {

        "education": education.strip(),

        "location": location.strip(),

        "skills": skills.strip(),

        "interests": interests.strip()

    }


    # --------------------------------------------------------
    # RUN AI ANALYSIS
    # --------------------------------------------------------

    with st.spinner(
        "Analyzing your profile and matching career opportunities..."
    ):

        try:

            result = run_career_analysis(
                profile_text,
                top_k=5
            )


            # ------------------------------------------------
            # SAVE RESULT
            # ------------------------------------------------

            st.session_state["career_result"] = result
            st.session_state["profile_input"] = {
              "education": education.strip(),
              "location": location.strip(),
              "skills": skills.strip(),
              "interests": interests.strip()
            }
            st.session_state["analysis_ready"] = True

            st.switch_page(
            "pages/analysis.py"
            )

            # ------------------------------------------------
            # DEBUG-SAFE CHECK
            # ------------------------------------------------

            if result is None:

                st.error(
                    "The career analysis returned no result. "
                    "Please try again."
                )

                st.stop()


            # ------------------------------------------------
            # MOVE TO ANALYSIS PAGE
            # ------------------------------------------------

            st.switch_page(
                "pages/analysis.py"
            )


        except Exception as e:

            st.error(
                f"Unable to analyze your profile: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    © Career Compass · Intelligent Career Navigation
</div>
""")