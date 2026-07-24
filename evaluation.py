# ==========================================================
# evaluation.py
# AI Interview Evaluation Engine
# ==========================================================

from similarity import similarity_engine
from keywords import keyword_engine
from grammar import grammar_engine
from sentiment import sentiment_engine


class InterviewEvaluator:

    def __init__(self):
        pass

    # ======================================================
    # Calculate Final Score
    # ======================================================

    def calculate_final_score(
        self,
        similarity_score,
        keyword_score,
        grammar_score
    ):
        """
        Weightage:
        Similarity : 50%
        Keywords   : 30%
        Grammar    : 20%
        """

        final_score = (
            (similarity_score * 0.50) +
            (keyword_score * 0.30) +
            (grammar_score * 0.20)
        )

        return round(final_score, 2)

    # ======================================================
    # Performance Remark
    # ======================================================

    def performance(self, score):

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "Very Good"

        elif score >= 60:
            return "Good"

        elif score >= 40:
            return "Average"

        else:
            return "Needs Improvement"

    # ======================================================
    # Evaluate Answer
    # ======================================================

    def evaluate(
        self,
        candidate_answer,
        expected_answer,
        keywords
    ):

        # -------------------------------
        # Similarity Score
        # -------------------------------

        similarity_result = similarity_engine.evaluate(
            candidate_answer,
            expected_answer
        )

        # -------------------------------
        # Keyword Score
        # -------------------------------

        keyword_result = keyword_engine.evaluate(
            candidate_answer,
            keywords
        )

        # -------------------------------
        # Grammar Score
        # -------------------------------

        grammar_result = grammar_engine.evaluate(
            candidate_answer
        )

        # -------------------------------
        # Sentiment
        # -------------------------------

        sentiment_result = sentiment_engine.analyze(
            candidate_answer
        )

        # -------------------------------
        # Final Score
        # -------------------------------

        final_score = self.calculate_final_score(
            similarity_result["score"],
            keyword_result["score"],
            grammar_result["score"]
        )

        remark = self.performance(final_score)

        # -------------------------------
        # Return Result
        # -------------------------------

        return {

            "similarity_score":
                similarity_result["score"],

            "similarity_remark":
                similarity_result["remark"],

            "keyword_score":
                keyword_result["score"],

            "matched_keywords":
                keyword_result["matched_keywords"],

            "grammar_score":
                grammar_result["score"],

            "grammar_errors":
                grammar_result["errors"],

            "grammar_remark":
                grammar_result["remark"],

            "sentiment":
                sentiment_result["sentiment"],

            "polarity":
                sentiment_result["polarity"],

            "subjectivity":
                sentiment_result["subjectivity"],

            "final_score":
                final_score,

            "overall_remark":
                remark

        }


# ==========================================================
# Create Object
# ==========================================================

evaluator = InterviewEvaluator()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    expected_answer = """
    Machine Learning is a branch of Artificial Intelligence
    that enables computers to learn from data without
    being explicitly programmed.
    """

    keywords = (
        "machine learning|artificial intelligence|"
        "data|algorithm|prediction"
    )

    print("=" * 60)
    print("AI Interview Evaluation Test")
    print("=" * 60)

    candidate_answer = input("\nEnter Candidate Answer:\n\n")

    result = evaluator.evaluate(
        candidate_answer,
        expected_answer,
        keywords
    )

    print("\n=========== RESULT ===========")

    print("Similarity Score :", result["similarity_score"], "%")
    print("Keyword Score    :", result["keyword_score"], "%")
    print("Grammar Score    :", result["grammar_score"], "%")
    print("Grammar Errors   :", result["grammar_errors"])
    print("Sentiment        :", result["sentiment"])
    print("Polarity         :", result["polarity"])
    print("Subjectivity     :", result["subjectivity"])
    print("Final Score      :", result["final_score"], "%")
    print("Overall Remark   :", result["overall_remark"])

    print("\nMatched Keywords:")

    if result["matched_keywords"]:

        for keyword in result["matched_keywords"]:

            print("✓", keyword)

    else:

        print("No keywords matched.")