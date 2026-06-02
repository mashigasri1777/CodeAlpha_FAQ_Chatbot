from flask import Flask, render_template, request, jsonify
import json
import os
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# IMPORTANT: Vercel needs this exact variable name
app = Flask(__name__)

# ----------------------------
# Load FAQ Data
# ----------------------------

faq_data = []

try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    faq_file = os.path.join(current_dir, "faq_data.json")

    with open(faq_file, "r", encoding="utf-8") as file:
        faq_data = json.load(file)

except Exception as e:
    print("FAQ Loading Error:", e)

# ----------------------------
# Prepare Questions & Answers
# ----------------------------

questions = []
answers = []

for item in faq_data:
    questions.append(item["question"])
    answers.append(item["answer"])

# ----------------------------
# Text Preprocessing
# ----------------------------

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

# ----------------------------
# TF-IDF Model
# ----------------------------

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

# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    if vectorizer is None:
        return jsonify({
            "answer": "FAQ database failed to load."
        })

    data = request.get_json()

    user_question = data.get(
        "question",
        ""
    ).strip()

    if user_question == "":
        return jsonify({
            "answer": "Please enter a question."
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

    best_match_index = similarity_scores.argmax()

    best_score = similarity_scores[0][best_match_index]

    if best_score < 0.15:
        return jsonify({
            "answer":
            "Sorry, I couldn't find a relevant answer. Please try asking about AI, Machine Learning, NLP, Deep Learning, Computer Vision, Python, Neural Networks, or Data Science."
        })

    return jsonify({
        "answer": answers[best_match_index]
    })


# ----------------------------
# Run App
# ----------------------------

if __name__ == "__main__":
    app.run(debug=True)
