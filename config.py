# =====================================================
# AI Interview Evaluator Configuration
# =====================================================

import os

# Database
DATABASE_NAME = "database/interview.db"

# Dataset
QUESTION_FILE = "dataset/questions.csv"

# Reports
CSV_REPORT = "reports/results.csv"
PDF_FOLDER = "pdf_reports"

# Application

APP_TITLE = "AI Interview Question Answer Evaluation System"

# Interview
QUESTIONS_PER_TEST = 10

# Directories
DIRECTORIES = [
    "database",
    "dataset",
    "reports",
    "pdf_reports",
    "assets",
    "screenshots"
]


def create_directories():
    """Create required project directories."""
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)