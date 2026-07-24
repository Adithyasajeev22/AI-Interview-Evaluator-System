# ==========================================================
# report.py
# CSV Report Generation Module
# ==========================================================

import os
import pandas as pd
from datetime import datetime
from config import CSV_REPORT


class ReportGenerator:

    def __init__(self):

        os.makedirs(os.path.dirname(CSV_REPORT), exist_ok=True)

    # ======================================================
    # Save Interview Result
    # ======================================================

    def save_result(
        self,
        candidate_name,
        email,
        category,
        question,
        answer,
        expected_answer,
        similarity,
        keyword_score,
        grammar_score,
        final_score,
        sentiment
    ):

        data = {

            "Date": [datetime.now().strftime("%Y-%m-%d")],

            "Time": [datetime.now().strftime("%H:%M:%S")],

            "Candidate": [candidate_name],

            "Email": [email],

            "Category": [category],

            "Question": [question],

            "Candidate_Answer": [answer],

            "Expected_Answer": [expected_answer],

            "Similarity_Score": [similarity],

            "Keyword_Score": [keyword_score],

            "Grammar_Score": [grammar_score],

            "Final_Score": [final_score],

            "Sentiment": [sentiment]

        }

        new_df = pd.DataFrame(data)

        if os.path.exists(CSV_REPORT):

            old_df = pd.read_csv(CSV_REPORT)

            final_df = pd.concat(
                [old_df, new_df],
                ignore_index=True
            )

        else:

            final_df = new_df

        final_df.to_csv(
            CSV_REPORT,
            index=False
        )

    # ======================================================
    # Load Reports
    # ======================================================

    def load_reports(self):

        if os.path.exists(CSV_REPORT):

            return pd.read_csv(CSV_REPORT)

        return pd.DataFrame()

    # ======================================================
    # Candidate History
    # ======================================================

    def candidate_history(self, email):

        df = self.load_reports()

        if df.empty:
            return df

        return df[df["Email"] == email]

    # ======================================================
    # Statistics
    # ======================================================

    def statistics(self):

        df = self.load_reports()

        if df.empty:

            return {

                "total_interviews": 0,

                "average_score": 0,

                "highest_score": 0,

                "lowest_score": 0

            }

        return {

            "total_interviews": len(df),

            "average_score": round(
                df["Final_Score"].mean(),
                2
            ),

            "highest_score": round(
                df["Final_Score"].max(),
                2
            ),

            "lowest_score": round(
                df["Final_Score"].min(),
                2
            )

        }

    # ======================================================
    # Top Candidates
    # ======================================================

    def top_candidates(
        self,
        limit=10
    ):

        df = self.load_reports()

        if df.empty:
            return df

        return df.sort_values(

            by="Final_Score",

            ascending=False

        ).head(limit)

    # ======================================================
    # Category Report
    # ======================================================

    def category_report(
        self,
        category
    ):

        df = self.load_reports()

        if df.empty:
            return df

        return df[
            df["Category"] == category
        ]

    # ======================================================
    # Delete All Reports
    # ======================================================

    def clear_reports(self):

        if os.path.exists(CSV_REPORT):

            os.remove(CSV_REPORT)


# ==========================================================
# Object
# ==========================================================

report = ReportGenerator()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    report.save_result(

        candidate_name="Adithya",

        email="adithya@gmail.com",

        category="Python",

        question="What is Python?",

        answer="Python is a programming language.",

        expected_answer="Python is a high-level programming language.",

        similarity=92,

        keyword_score=90,

        grammar_score=95,

        final_score=92.6,

        sentiment="Positive"

    )

    print(report.load_reports())

    print(report.statistics())

    print(report.top_candidates())
    