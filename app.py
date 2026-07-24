# ==========================================================
# app.py
# AI Interview Question Answer Evaluation System
# ==========================================================

import streamlit as st

from login import login_page, logout
from register import register_page
from interview import interview_page, evaluate_interview
from dashboard import dashboard

# ==========================================================
# Streamlit Configuration
# ==========================================================

st.set_page_config(
    page_title="AI Interview Question Answer Evaluation System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Session State Initialization
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "completed" not in st.session_state:
    st.session_state.completed = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("🤖 AI Interview Evaluator")

st.sidebar.markdown("---")

# ==========================================================
# Home Page
# ==========================================================

if not st.session_state.logged_in:

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "🔐 Login",
            "📝 Register"
        ]
    )

    if menu == "🏠 Home":

        st.title("AI Interview Question Answer Evaluation System")

        st.write("""
Welcome to the AI-powered Interview Evaluation Platform.

### Features

- AI-based Answer Evaluation
- TF-IDF Similarity
- Keyword Matching
- Grammar Checking
- Sentiment Analysis
- Performance Dashboard
- PDF Report Generation
- CSV Report Export
- SQLite Database

### Technologies

- Python
- Streamlit
- Scikit-learn
- TextBlob
- LanguageTool
- SQLite
- Pandas
- ReportLab
        """)

    elif menu == "🔐 Login":

        login_page()

    elif menu == "📝 Register":

        register_page()

# ==========================================================
# Logged-in User
# ==========================================================

else:

    st.sidebar.success(
        f"Welcome,\n{st.session_state.user_name}"
    )

    menu = st.sidebar.radio(

        "Navigation",

        [

            "🎤 Start Interview",

            "📊 Dashboard",

            "🚪 Logout"

        ]

    )

    # ------------------------------------------------------

    if menu == "🎤 Start Interview":

        if st.session_state.completed:

            evaluate_interview()

        else:

            interview_page()

    # ------------------------------------------------------

    elif menu == "📊 Dashboard":

        dashboard()

    # ------------------------------------------------------

    elif menu == "🚪 Logout":

        logout()

# ==========================================================
# Footer
# ==========================================================

st.sidebar.markdown("---")

st.sidebar.info(
    """
AI Interview Question Answer Evaluation System

Version : 1.0

Developed using

• Python

• Streamlit

• Scikit-learn

• TextBlob

• SQLite
"""
)