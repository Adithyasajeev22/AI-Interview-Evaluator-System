# ==========================================================
# similarity.py
# TF-IDF + Cosine Similarity
# ==========================================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

    def preprocess(self, text):

        if text is None:
            return ""

        text = text.lower().strip()

        return text

    def calculate_similarity(
        self,
        candidate_answer,
        expected_answer
    ):

        candidate_answer = self.preprocess(candidate_answer)
        expected_answer = self.preprocess(expected_answer)

        if candidate_answer == "":
            return 0.0

        documents = [
            candidate_answer,
            expected_answer
        ]

        tfidf_matrix = self.vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )

        score = similarity[0][0] * 100

        return round(score, 2)

    def evaluate(
        self,
        candidate_answer,
        expected_answer
    ):

        score = self.calculate_similarity(
            candidate_answer,
            expected_answer
        )

        if score >= 85:
            remark = "Excellent"

        elif score >= 70:
            remark = "Very Good"

        elif score >= 50:
            remark = "Good"

        elif score >= 30:
            remark = "Average"

        else:
            remark = "Poor"

        return {
            "score": score,
            "remark": remark
        }


similarity_engine = SimilarityEngine()


if __name__ == "__main__":

    expected = """
    Machine Learning is a branch of Artificial Intelligence
    that enables computers to learn from data without
    explicit programming.
    """

    answer = input("Enter Candidate Answer:\n")

    result = similarity_engine.evaluate(
        answer,
        expected
    )

    print("\nSimilarity Score:", result["score"])
    print("Performance:", result["remark"])