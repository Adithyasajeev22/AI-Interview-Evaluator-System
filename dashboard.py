# ==========================================================
# dashboard.py
# Imports, Data Loading, KPI Cards
# ==========================================================

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from database import db
from config import CSV_REPORT


# ==========================================================
# Streamlit Page
# ==========================================================

st.set_page_config(
    page_title="AI Interview Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# Load CSV Reports
# ==========================================================

@st.cache_data
def load_reports():

    if os.path.exists(CSV_REPORT):

        df = pd.read_csv(CSV_REPORT)

    else:

        df = pd.DataFrame(
            columns=[
                "Date",
                "Time",
                "Candidate",
                "Email",
                "Category",
                "Question",
                "Candidate_Answer",
                "Expected_Answer",
                "Similarity_Score",
                "Keyword_Score",
                "Grammar_Score",
                "Final_Score",
                "Sentiment"
            ]
        )

    return df


# ==========================================================
# Dashboard Header
# ==========================================================

def dashboard():

    st.title("🤖 AI Interview Evaluation Dashboard")

    st.markdown(
        "Real-time analytics for candidate interview performance."
    )

    st.markdown("---")

    df = load_reports()

    # ======================================================
    # KPI Cards
    # ======================================================

    total_candidates = db.total_users()

    total_interviews = db.total_results()

    average_score = db.average_score()

    highest_score = db.highest_score()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="👥 Total Candidates",
            value=total_candidates
        )

    with col2:

        st.metric(
            label="📝 Interviews",
            value=total_interviews
        )

    with col3:

        st.metric(
            label="📈 Average Score",
            value=f"{average_score}%"
        )

    with col4:

        st.metric(
            label="🏆 Highest Score",
            value=f"{highest_score}%"
        )

    st.markdown("---")

    # ======================================================
    # Quick Statistics
    # ======================================================

    if not df.empty:

        left, right = st.columns(2)

        with left:

            st.subheader("Interview Statistics")

            st.write(
                f"**Total Reports :** {len(df)}"
            )

            st.write(
                f"**Average Score :** "
                f"{round(df['Final_Score'].mean(),2)}%"
            )

            st.write(
                f"**Highest Score :** "
                f"{round(df['Final_Score'].max(),2)}%"
            )

            st.write(
                f"**Lowest Score :** "
                f"{round(df['Final_Score'].min(),2)}%"
            )

        with right:

            st.subheader("Category Distribution")

            if "Category" in df.columns:

                st.write(
                    df["Category"].value_counts()
                )

    else:

        st.info("No interview records available.")

    st.markdown("---")
# ==========================================================
# dashboard.py
# Charts and Analytics
# ==========================================================

    # ======================================================
    # Category-wise Average Score
    # ======================================================

    if not df.empty and "Category" in df.columns:

        st.subheader("📊 Category-wise Average Score")

        category_scores = (
            df.groupby("Category")["Final_Score"]
            .mean()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            category_scores.index,
            category_scores.values
        )

        ax.set_xlabel("Category")
        ax.set_ylabel("Average Score")
        ax.set_title("Average Score by Category")

        plt.xticks(rotation=45)

        st.pyplot(fig)

    # ======================================================
    # Interview Category Distribution
    # ======================================================

    if not df.empty and "Category" in df.columns:

        st.subheader("🥧 Interview Category Distribution")

        category_count = df["Category"].value_counts()

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.pie(
            category_count.values,
            labels=category_count.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Interview Categories")

        st.pyplot(fig)

    # ======================================================
    # Candidate Score Trend
    # ======================================================

    if not df.empty:

        st.subheader("📈 Candidate Score Trend")

        score_df = df.copy()

        score_df = score_df.reset_index(drop=True)

        score_df["Interview_No"] = score_df.index + 1

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            score_df["Interview_No"],
            score_df["Final_Score"],
            marker="o"
        )

        ax.set_xlabel("Interview Number")
        ax.set_ylabel("Final Score")
        ax.set_title("Interview Performance Trend")

        st.pyplot(fig)

    # ======================================================
    # Score Distribution
    # ======================================================

    if not df.empty:

        st.subheader("📉 Score Distribution")

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.hist(
            df["Final_Score"],
            bins=10
        )

        ax.set_xlabel("Final Score")
        ax.set_ylabel("Number of Candidates")
        ax.set_title("Distribution of Interview Scores")

        st.pyplot(fig)

    # ======================================================
    # Similarity vs Grammar
    # ======================================================

    if not df.empty:

        st.subheader("📌 Similarity vs Grammar Score")

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.scatter(
            df["Similarity_Score"],
            df["Grammar_Score"]
        )

        ax.set_xlabel("Similarity Score")

        ax.set_ylabel("Grammar Score")

        ax.set_title("Similarity vs Grammar")

        st.pyplot(fig)

    st.markdown("---")  
# ==========================================================
# dashboard.py
# Part 3
# Candidate Search, Top Candidates, Reports
# ==========================================================

    # ======================================================
    # Candidate Search
    # ======================================================

    st.subheader("🔍 Search Candidate")

    search_name = st.text_input(
        "Enter Candidate Name"
    )

    if search_name:

        result = df[
            df["Candidate"]
            .str.contains(
                search_name,
                case=False,
                na=False
            )
        ]

        if not result.empty:

            st.success(
                f"{len(result)} record(s) found."
            )

            st.dataframe(
                result,
                use_container_width=True
            )

        else:

            st.warning(
                "No candidate found."
            )

    st.markdown("---")

    # ======================================================
    # Top 10 Candidates
    # ======================================================

    st.subheader("🏆 Top 10 Candidates")

    if not df.empty:

        top_candidates = (
            df.sort_values(
                by="Final_Score",
                ascending=False
            )
            .drop_duplicates(
                subset=["Candidate"]
            )
            .head(10)
        )

        st.dataframe(
            top_candidates[
                [
                    "Candidate",
                    "Category",
                    "Final_Score"
                ]
            ],
            use_container_width=True
        )

    else:

        st.info("No interview reports available.")

    st.markdown("---")

    # ======================================================
    # Candidate Performance Summary
    # ======================================================

    st.subheader("📊 Candidate Performance Summary")

    if not df.empty:

        summary = (
            df.groupby("Candidate")
            .agg(
                Interviews=("Candidate", "count"),
                Average_Score=("Final_Score", "mean"),
                Highest_Score=("Final_Score", "max")
            )
            .reset_index()
        )

        summary["Average_Score"] = (
            summary["Average_Score"]
            .round(2)
        )

        st.dataframe(
            summary,
            use_container_width=True
        )

    st.markdown("---")

    # ======================================================
    # Full Interview Records
    # ======================================================

    st.subheader("📋 Interview Records")

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning("No records found.")

    st.markdown("---")

    # ======================================================
    # Download CSV Report
    # ======================================================

    st.subheader("⬇ Download Reports")

    csv = df.to_csv(index=False)

    st.download_button(

        label="Download CSV Report",

        data=csv,

        file_name="Interview_Report.csv",

        mime="text/csv"

    )

    st.markdown("---")    
# ==========================================================
# dashboard.py
# Part 4
# Admin Analytics, Report Management & Main Function
# ==========================================================

    # ======================================================
    # Overall Performance Analysis
    # ======================================================

    st.subheader("📈 Overall Performance")

    if not df.empty:

        excellent = len(df[df["Final_Score"] >= 90])

        very_good = len(df[
            (df["Final_Score"] >= 75) &
            (df["Final_Score"] < 90)
        ])

        good = len(df[
            (df["Final_Score"] >= 60) &
            (df["Final_Score"] < 75)
        ])

        average = len(df[
            (df["Final_Score"] >= 40) &
            (df["Final_Score"] < 60)
        ])

        poor = len(df[df["Final_Score"] < 40])

        performance = {
            "Excellent": excellent,
            "Very Good": very_good,
            "Good": good,
            "Average": average,
            "Needs Improvement": poor
        }

        performance_df = pd.DataFrame(
            performance.items(),
            columns=["Performance", "Candidates"]
        )

        st.dataframe(
            performance_df,
            use_container_width=True
        )

    st.markdown("---")

    # ======================================================
    # Interview Category Filter
    # ======================================================

    if not df.empty:

        st.subheader("📂 Filter by Category")

        categories = ["All"] + sorted(
            df["Category"].dropna().unique().tolist()
        )

        selected_category = st.selectbox(
            "Select Category",
            categories
        )

        if selected_category != "All":

            filtered = df[
                df["Category"] == selected_category
            ]

            st.dataframe(
                filtered,
                use_container_width=True
            )

        else:

            st.dataframe(
                df,
                use_container_width=True
            )

    st.markdown("---")

    # ======================================================
    # Admin Controls
    # ======================================================

    st.subheader("⚙ Admin Controls")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🔄 Refresh Dashboard"):

            st.cache_data.clear()

            st.success(
                "Dashboard refreshed successfully."
            )

            st.rerun()

    with col2:

        if st.button("🗑 Clear All Reports"):

            try:

                empty_df = pd.DataFrame(
                    columns=df.columns
                )

                empty_df.to_csv(
                    CSV_REPORT,
                    index=False
                )

                st.success(
                    "All reports cleared successfully."
                )

                st.cache_data.clear()

                st.rerun()

            except Exception as e:

                st.error(str(e))

    st.markdown("---")

    # ======================================================
    # Dashboard Footer
    # ======================================================

    st.caption(
        "AI Interview Question Answer Evaluation System"
    )

    st.caption(
        "Developed using Python, Streamlit, "
        "Scikit-learn, TextBlob, Pandas and SQLite."
    )


# ==========================================================
# Run Dashboard
# ==========================================================

if __name__ == "__main__":

    dashboard()      