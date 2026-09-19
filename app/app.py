import streamlit as st

st.set_page_config(
    page_title="Career Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background: #F7F9FC;
}

[data-testid="stSidebar"] {
    display: none;
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

.main .block-container {
    max-width: 1200px;
    padding-top: 0.5rem;
    padding-bottom: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# PAGES
# ============================================================

home = st.Page(
    "pages/home.py",
    title="Dashboard",
    icon="🏠"
)

profile = st.Page(
    "pages/profile.py",
    title="Profile",
    icon="👤"
)

analysis = st.Page(
    "pages/analysis.py",
    title="AI Analysis",
    icon="🤖"
)

jobs = st.Page(
    "pages/jobs.py",
    title="Jobs",
    icon="💼"
)

job_details = st.Page(
    "pages/job_details.py",
    title="Job Details",
    icon="📄"
)

skill_gaps = st.Page(
    "pages/skill_gaps.py",
    title="Skill Gaps",
    icon="🎯"
)

learning = st.Page(
    "pages/learning_path.py",
    title="Learning Path",
    icon="📚"
)


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    [
        home,
        profile,
        analysis,
        jobs,
        job_details,
        skill_gaps,
        learning
    ],
    position="hidden"
)

pg.run()