from flask import Flask, render_template, request, jsonify
import json
import string
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

faq_path = os.path.join(BASE_DIR, "faq_data.json")

with open(faq_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)
    
    from flask import Flask, render_template, request, jsonify
import json
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load FAQ Data
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# Text Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

processed_questions = [preprocess_text(q) for q in questions]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words="english")
question_vectors = vectorizer.fit_transform(processed_questions)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({
            "answer": "Please enter a question.",
            "confidence": 0
        })

    # Preprocess user input
    processed_input = preprocess_text(user_question)

    # Convert to vector
    user_vector = vectorizer.transform([processed_input])

    # Calculate similarity
    similarity_scores = cosine_similarity(
        user_vector,
        question_vectors
    )

    # Best match
    best_match_index = similarity_scores.argmax()
    best_score = similarity_scores[0][best_match_index]

    confidence = round(best_score * 100, 2)

    # Fallback response
    if best_score < 0.20:
        return jsonify({
            "answer": "Sorry, I couldn't find a matching FAQ. Try asking about Artificial Intelligence, Machine Learning, Deep Learning, NLP, Python, Data Science, Computer Vision, or Neural Networks.",
            "confidence": confidence,
            "matched_question": "No Match Found"
        })

    return jsonify({
        "answer": answers[best_match_index],
        "confidence": confidence,
        "matched_question": questions[best_match_index]
    })

if __name__ == "__main__":
    app.run(debug=True)
