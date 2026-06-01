from flask import Flask, render_template, request, jsonify
import json
import string
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# -----------------------------
# Load FAQ Data Safely
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAQ_FILE = os.path.join(BASE_DIR, "faq_data.json")

try:
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        faq_data = json.load(f)
except Exception as e:
    print("FAQ Loading Error:", e)
    faq_data = []

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# -----------------------------
# Text Preprocessing
# -----------------------------

def preprocess_text(text):
    text = text.lower()
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )
    return text

processed_questions = [
    preprocess_text(q)
    for q in questions
]

# -----------------------------
# TF-IDF Setup
# -----------------------------

if processed_questions:

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    question_vectors = vectorizer.fit_transform(
        processed_questions
    )

else:

    vectorizer = None
    question_vectors = None

# -----------------------------
# Home Page
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Chatbot API
# -----------------------------

@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        user_question = data.get(
            "question",
            ""
        ).strip()

        if not user_question:

            return jsonify({
                "answer":
                "Please enter a question.",
                "confidence": 0
            })

        if not vectorizer:

            return jsonify({
                "answer":
                "FAQ database failed to load.",
                "confidence": 0
            })

        processed_input = preprocess_text(
            user_question
        )

        user_vector = vectorizer.transform(
            [processed_input]
        )

        similarity_scores = cosine_similarity(
            user_vector,
            question_vectors
        )

        best_match_index = (
            similarity_scores.argmax()
        )

        best_score = (
            similarity_scores[0][best_match_index]
        )

        confidence = round(
            best_score * 100,
            2
        )

        if best_score < 0.20:

            return jsonify({

                "answer":
                "Sorry, I couldn't find a matching FAQ. Try asking about Artificial Intelligence, Machine Learning, Deep Learning, NLP, Data Science, Python, Neural Networks, or Computer Vision.",

                "confidence":
                confidence,

                "matched_question":
                "No Match Found"

            })

        return jsonify({

            "answer":
            answers[best_match_index],

            "confidence":
            confidence,

            "matched_question":
            questions[best_match_index]

        })

    except Exception as e:

        print("CHATBOT ERROR:", e)

        return jsonify({

            "answer":
            "Internal server error occurred.",

            "confidence":
            0

        })

# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
