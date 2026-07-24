# ==========================================================
# sentiment.py
# Sentiment Analysis Module
# ==========================================================

from textblob import TextBlob


class SentimentAnalyzer:

    def __init__(self):
        pass

    def analyze(self, text):
        """
        Analyze the sentiment of the given text.
        Returns sentiment label, polarity, and subjectivity.
        """

        text = text.strip()

        if text == "":
            return {
                "sentiment": "Neutral",
                "polarity": 0.0,
                "subjectivity": 0.0
            }

        blob = TextBlob(text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        if polarity > 0.2:
            sentiment = "Positive"

        elif polarity < -0.2:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity
        }

    def detailed_report(self, text):
        """
        Generate a detailed sentiment report.
        """

        result = self.analyze(text)

        report = {
            "Sentiment": result["sentiment"],
            "Polarity": result["polarity"],
            "Subjectivity": result["subjectivity"]
        }

        return report


# ==========================================================
# Create Object
# ==========================================================

sentiment_engine = SentimentAnalyzer()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Sentiment Analysis")
    print("=" * 60)

    answer = input("\nEnter Candidate Answer:\n\n")

    result = sentiment_engine.analyze(answer)

    print("\n========== Sentiment Result ==========")
    print("Sentiment    :", result["sentiment"])
    print("Polarity     :", result["polarity"])
    print("Subjectivity :", result["subjectivity"])