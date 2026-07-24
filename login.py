# ==========================================================
# login.py
# Candidate Login Module
# ==========================================================

import streamlit as st
from database import db


def login_page():

    st.title("🔐 Candidate Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = db.login_user(
            email,
            password
        )

        if user:

            st.success("Login Successful")

            st.session_state["logged_in"] = True

            st.session_state["user_name"] = user[1]

            st.session_state["user_email"] = user[2]

            st.rerun()

        else:

            st.error("Invalid Email or Password")


def logout():

    st.session_state.clear()

    st.success("Logged Out Successfully")

    st.rerun()