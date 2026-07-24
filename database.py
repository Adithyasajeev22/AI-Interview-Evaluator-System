# =====================================================
# Database Module
# =====================================================

import sqlite3
from config import DATABASE_NAME, create_directories


create_directories()


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(
            DATABASE_NAME,
            check_same_thread=False
        )
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):

        # -------------------------------
        # Users Table
        # -------------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
        """)

        # -------------------------------
        # Interview Results
        # -------------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS results(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_email TEXT,

            category TEXT,

            score REAL,

            similarity REAL,

            grammar REAL,

            sentiment TEXT,

            interview_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.connection.commit()

    # ===================================
    # User Registration
    # ===================================

    def register_user(self, name, email, password):

        try:

            self.cursor.execute(
                """
                INSERT INTO users(name,email,password)
                VALUES(?,?,?)
                """,
                (name, email, password)
            )

            self.connection.commit()

            return True

        except sqlite3.IntegrityError:

            return False

    # ===================================
    # User Login
    # ===================================

    def login_user(self, email, password):

        self.cursor.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email, password)
        )

        return self.cursor.fetchone()

    # ===================================
    # Save Result
    # ===================================

    def save_result(
        self,
        user_email,
        category,
        score,
        similarity,
        grammar,
        sentiment
    ):

        self.cursor.execute(
            """
            INSERT INTO results
            (
                user_email,
                category,
                score,
                similarity,
                grammar,
                sentiment
            )

            VALUES(?,?,?,?,?,?)
            """,
            (
                user_email,
                category,
                score,
                similarity,
                grammar,
                sentiment
            )
        )

        self.connection.commit()

    # ===================================
    # Get Results
    # ===================================

    def get_results(self, email):

        self.cursor.execute(
            """
            SELECT *
            FROM results
            WHERE user_email=?
            ORDER BY interview_date DESC
            """,
            (email,)
        )

        return self.cursor.fetchall()

    # ===================================
    # Dashboard Statistics
    # ===================================

    def total_users(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        return self.cursor.fetchone()[0]

    def total_results(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM results"
        )

        return self.cursor.fetchone()[0]

    def average_score(self):

        self.cursor.execute(
            "SELECT AVG(score) FROM results"
        )

        value = self.cursor.fetchone()[0]

        return round(value, 2) if value else 0

    def highest_score(self):

        self.cursor.execute(
            "SELECT MAX(score) FROM results"
        )

        value = self.cursor.fetchone()[0]

        return round(value, 2) if value else 0

    # ===================================
    # Close Connection
    # ===================================

    def close(self):

        self.connection.close()


# Singleton instance
db = Database()