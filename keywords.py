# ==========================================================
# keywords.py
# Keyword Matching Module
# ==========================================================

import re


class KeywordMatcher:

    def __init__(self):
        pass

    def preprocess(self, text):
        """
        Convert text to lowercase and remove special characters.
        """
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_keywords(self, keyword_string):
        """
        Convert:
        python|language|programming
        into
        ['python','language','programming']
        """

        if keyword_string is None:
            return []

        keywords = [
            word.strip().lower()
            for word in keyword_string.split("|")
            if word.strip()
        ]

        return keywords

    def keyword_score(self, candidate_answer, keyword_string):

        candidate_answer = self.preprocess(candidate_answer)

        keywords = self.extract_keywords(keyword_string)

        if len(keywords) == 0:
            return 0, []

        matched = []

        for keyword in keywords:

            if keyword in candidate_answer:
                matched.append(keyword)

        score = (len(matched) / len(keywords)) * 100

        return round(score, 2), matched

    def evaluate(self, candidate_answer, keyword_string):

        score, matched = self.keyword_score(
            candidate_answer,
            keyword_string
        )

        if score >= 90:
            remark = "Excellent"

        elif score >= 75:
            remark = "Very Good"

        elif score >= 50:
            remark = "Good"

        elif score >= 25:
            remark = "Average"

        else:
            remark = "Poor"

        return {
            "score": score,
            "matched_keywords": matched,
            "total_keywords": len(
                self.extract_keywords(keyword_string)
            ),
            "remark": remark
        }


keyword_engine = KeywordMatcher()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    expected_keywords = (
        "machine learning|artificial intelligence|"
        "data|algorithm|prediction"
    )

    answer = input("Enter Candidate Answer:\n")

    result = keyword_engine.evaluate(
        answer,
        expected_keywords
    )

    print("\n========== Keyword Evaluation ==========")
    print("Keyword Score :", result["score"], "%")
    print("Matched Keywords :", result["matched_keywords"])
    print("Total Keywords :", result["total_keywords"])
    print("Performance :", result["remark"])