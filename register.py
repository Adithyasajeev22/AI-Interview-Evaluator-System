# ==========================================================
# register.py
# Candidate Registration Module
# ==========================================================

import re
import streamlit as st
from database import db


def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)


def is_strong_password(password):
    """
    Minimum 8 characters
    At least one uppercase
    At least one lowercase
    At least one digit
    """

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True


def register_page():

    st.title("📝 Candidate Registration")

    st.write("Create your account to attend AI Interview Evaluation.")

    name = st.text_input("Full Name")

    email = st.text_input("Email Address")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if not name.strip():
            st.error("Enter your name.")
            return

        if not is_valid_email(email):
            st.error("Invalid email address.")
            return

        if not is_strong_password(password):
            st.error(
                """
Password must contain:

• Minimum 8 characters

• One uppercase letter

• One lowercase letter

• One number
"""
            )
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        success = db.register_user(
            name,
            email,
            password
        )

        if success:

            st.success("Registration Successful!")

            st.info("Go to Login Page.")

        else:

            st.error("Email already exists.")