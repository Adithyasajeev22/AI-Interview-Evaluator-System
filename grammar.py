import re

class GrammarEngine:

    def evaluate(self, text):

        if not text.strip():
            return {
                "score": 0,
                "errors": 0,
                "remark": "No Answer"
            }

        errors = 0

        if not text[0].isupper():
            errors += 1

        if text[-1] not in ".!?":
            errors += 1

        errors += len(re.findall(r"\s{2,}", text))

        score = max(0, 100 - errors * 10)

        if score >= 90:
            remark = "Excellent"
        elif score >= 75:
            remark = "Very Good"
        elif score >= 60:
            remark = "Good"
        elif score >= 40:
            remark = "Average"
        else:
            remark = "Needs Improvement"

        return {
            "score": score,
            "errors": errors,
            "remark": remark
        }

grammar_engine = GrammarEngine()