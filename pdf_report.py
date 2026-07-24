# ==========================================================
# pdf_report.py
# Professional PDF Report Generator
# ==========================================================

import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from config import PDF_FOLDER


class PDFReportGenerator:

    def __init__(self):

        os.makedirs(PDF_FOLDER, exist_ok=True)

        self.styles = getSampleStyleSheet()

    # ======================================================
    # Generate PDF
    # ======================================================

    def generate_report(
        self,
        candidate_name,
        email,
        category,
        results
    ):
        """
        results = [
            {
                "question": "...",
                "candidate_answer": "...",
                "expected_answer": "...",
                "similarity": 90,
                "keyword": 85,
                "grammar": 95,
                "sentiment": "Positive",
                "final_score": 90
            }
        ]
        """

        filename = f"{candidate_name.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        filepath = os.path.join(PDF_FOLDER, filename)

        document = SimpleDocTemplate(filepath)

        story = []

        # --------------------------------------------------

        title = Paragraph(
            "<b><font size=18>"
            "AI Interview Evaluation Report"
            "</font></b>",
            self.styles["Title"]
        )

        story.append(title)

        story.append(Spacer(1, 20))

        # --------------------------------------------------

        info = [

            ["Candidate", candidate_name],

            ["Email", email],

            ["Category", category],

            ["Generated On",
             datetime.now().strftime("%d-%m-%Y %H:%M:%S")]

        ]

        table = Table(info, colWidths=[140, 330])

        table.setStyle(TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

        ]))

        story.append(table)

        story.append(Spacer(1, 20))

        total_score = 0

        # ==================================================
        # Question Wise Report
        # ==================================================

        for i, item in enumerate(results, start=1):

            story.append(

                Paragraph(
                    f"<b>Question {i}</b>",
                    self.styles["Heading2"]
                )

            )

            story.append(
                Paragraph(
                    f"<b>Question:</b> {item['question']}",
                    self.styles["BodyText"]
                )
            )

            story.append(
                Paragraph(
                    f"<b>Candidate Answer:</b> "
                    f"{item['candidate_answer']}",
                    self.styles["BodyText"]
                )
            )

            story.append(
                Paragraph(
                    f"<b>Expected Answer:</b> "
                    f"{item['expected_answer']}",
                    self.styles["BodyText"]
                )
            )

            score_table = [

                ["Similarity", item["similarity"]],

                ["Keyword Score", item["keyword"]],

                ["Grammar Score", item["grammar"]],

                ["Sentiment", item["sentiment"]],

                ["Final Score", item["final_score"]]

            ]

            t = Table(score_table, colWidths=[180, 120])

            t.setStyle(TableStyle([

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 0), (0, -1),
                 colors.whitesmoke),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

            ]))

            story.append(t)

            story.append(Spacer(1, 18))

            total_score += item["final_score"]

        # ==================================================
        # Overall Summary
        # ==================================================

        average = round(total_score / len(results), 2)

        if average >= 90:
            remark = "Excellent"

        elif average >= 75:
            remark = "Very Good"

        elif average >= 60:
            remark = "Good"

        elif average >= 40:
            remark = "Average"

        else:
            remark = "Needs Improvement"

        summary = [

            ["Average Score", average],

            ["Overall Result", remark]

        ]

        summary_table = Table(summary, colWidths=[180, 180])

        summary_table.setStyle(TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (0, -1),
             colors.lightblue),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold")

        ]))

        story.append(summary_table)

        story.append(Spacer(1, 20))

        story.append(

            Paragraph(

                "<b>Thank you for using AI Interview "
                "Question Answer Evaluation System.</b>",

                self.styles["Heading3"]

            )

        )

        document.build(story)

        return filepath


# ==========================================================
# Object
# ==========================================================

pdf_generator = PDFReportGenerator()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    sample_results = [

        {

            "question":
                "What is Machine Learning?",

            "candidate_answer":
                "Machine Learning enables computers to learn from data.",

            "expected_answer":
                "Machine Learning is a branch of AI that enables systems "
                "to learn from data without explicit programming.",

            "similarity": 91,

            "keyword": 88,

            "grammar": 96,

            "sentiment": "Positive",

            "final_score": 91.2

        }

    ]

    path = pdf_generator.generate_report(

        candidate_name="Adithya V S",

        email="adithya@example.com",

        category="Machine Learning",

        results=sample_results

    )

    print("PDF Generated Successfully:")
    print(path)