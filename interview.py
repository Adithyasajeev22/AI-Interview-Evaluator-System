# ==========================================================
# interview.py
# Part 1
# ==========================================================

import random
import pandas as pd
import streamlit as st

from evaluation import evaluator
from database import db
from config import QUESTION_FILE, QUESTIONS_PER_TEST


# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_questions():

    df = pd.read_csv(QUESTION_FILE)

    return df


# ==========================================================
# Select Random Questions
# ==========================================================

def get_random_questions():

    df = load_questions()

    if len(df) < QUESTIONS_PER_TEST:

        return df.to_dict("records")

    selected = df.sample(
        n=QUESTIONS_PER_TEST,
        random_state=random.randint(1, 10000)
    )

    return selected.to_dict("records")


# ==========================================================
# Session Initialization
# ==========================================================

def initialize_session():

    if "questions" not in st.session_state:

        st.session_state.questions = get_random_questions()

    if "current_question" not in st.session_state:

        st.session_state.current_question = 0

    if "answers" not in st.session_state:

        st.session_state.answers = {}

    if "scores" not in st.session_state:

        st.session_state.scores = []

    if "completed" not in st.session_state:

        st.session_state.completed = False


# ==========================================================
# Progress Bar
# ==========================================================

def show_progress():

    current = st.session_state.current_question + 1

    total = len(st.session_state.questions)

    progress = current / total

    st.progress(progress)

    st.write(f"Question {current} of {total}")
# ==========================================================
# interview.py
# Part 2
# ==========================================================

def interview_page():

    initialize_session()

    questions = st.session_state.questions

    index = st.session_state.current_question

    question = questions[index]

    show_progress()

    st.markdown("---")

    st.subheader(f"Question {index + 1}")

    st.write(question["Question"])

    previous_answer = st.session_state.answers.get(index, "")

    answer = st.text_area(
        "Enter your answer",
        value=previous_answer,
        height=200,
        key=f"answer_{index}"
    )

    st.session_state.answers[index] = answer

    col1, col2, col3 = st.columns(3)

    # ======================================
    # Previous Button
    # ======================================

    with col1:

        if st.button("⬅ Previous"):

            if index > 0:

                st.session_state.current_question -= 1

                st.rerun()

    # ======================================
    # Save Answer
    # ======================================

    with col2:

        if st.button("💾 Save Answer"):

            st.session_state.answers[index] = answer

            st.success("Answer saved successfully.")

    # ======================================
    # Next Button
    # ======================================

    with col3:

        if index < len(questions) - 1:

            if st.button("Next ➡"):

                st.session_state.answers[index] = answer

                st.session_state.current_question += 1

                st.rerun()

    st.markdown("---")

    answered = len([
        a for a in st.session_state.answers.values()
        if str(a).strip() != ""
    ])

    st.info(
        f"Answered Questions: {answered}/{len(questions)}"
    )

    # ======================================
    # Show Submit Button only on Last Question
    # ======================================

    if index == len(questions) - 1:

        st.warning(
            "You have reached the last question."
        )

        if st.button(
            "✅ Submit Interview",
            type="primary",
            use_container_width=True
        ):

            st.session_state.completed = True

            st.rerun()
# ==========================================================
# interview.py
# Part 3
# ==========================================================

def evaluate_interview():

    st.title("📊 Interview Result")

    questions = st.session_state.questions
    answers = st.session_state.answers

    total_score = 0
    total_similarity = 0
    total_grammar = 0

    st.session_state.scores = []

    for index, question in enumerate(questions):

        candidate_answer = answers.get(index, "")

        expected_answer = question["Expected_Answer"]

        keywords = question["Keywords"]

        result = evaluator.evaluate(
            candidate_answer,
            expected_answer,
            keywords
        )

        st.session_state.scores.append(result)

        total_score += result["final_score"]
        total_similarity += result["similarity_score"]
        total_grammar += result["grammar_score"]

        with st.expander(f"Question {index+1}"):

            st.write("### Question")
            st.write(question["Question"])

            st.write("### Your Answer")
            st.write(candidate_answer)

            st.write("### Expected Answer")
            st.write(expected_answer)

            st.metric(
                "Final Score",
                f"{result['final_score']}%"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Similarity",
                    f"{result['similarity_score']}%"
                )

                st.metric(
                    "Grammar",
                    f"{result['grammar_score']}%"
                )

            with col2:

                st.metric(
                    "Keyword",
                    f"{result['keyword_score']}%"
                )

                st.metric(
                    "Sentiment",
                    result["sentiment"]
                )

            st.write("Matched Keywords")

            if result["matched_keywords"]:

                st.success(
                    ", ".join(result["matched_keywords"])
                )

            else:

                st.error("No keywords matched.")

            st.info(
                f"Overall Remark : {result['overall_remark']}"
            )

    total_questions = len(questions)

    average_score = round(
        total_score / total_questions,
        2
    )

    average_similarity = round(
        total_similarity / total_questions,
        2
    )

    average_grammar = round(
        total_grammar / total_questions,
        2
    )

    st.markdown("---")

    st.header("Overall Performance")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Score",
        f"{average_score}%"
    )

    c2.metric(
        "Similarity",
        f"{average_similarity}%"
    )

    c3.metric(
        "Grammar",
        f"{average_grammar}%"
    )

    if average_score >= 90:

        remark = "Excellent"

    elif average_score >= 75:

        remark = "Very Good"

    elif average_score >= 60:

        remark = "Good"

    elif average_score >= 40:

        remark = "Average"

    else:

        remark = "Needs Improvement"

    st.success(
        f"Overall Result : {remark}"
    )

    # ==========================================
    # Save Interview Result
    # ==========================================

    email = st.session_state.get(
        "user_email",
        "guest@example.com"
    )

    db.save_result(

        user_email=email,

        category="General",

        score=average_score,

        similarity=average_similarity,

        grammar=average_grammar,

        sentiment=remark

    )

    st.success(
        "Interview results saved successfully."
    )


# ==========================================================
# Main Entry
# ==========================================================

if __name__ == "__main__":

    if "completed" not in st.session_state:

        st.session_state.completed = False

    if st.session_state.completed:

        evaluate_interview()

    else:

        interview_page()
        
                        