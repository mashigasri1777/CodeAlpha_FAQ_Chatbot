from flask import Flask, render_template, request, jsonify
import json
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

processed_questions = [preprocess_text(q) for q in questions]

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
        return jsonify({"answer": "Please enter a question."})

    processed_input = preprocess_text(user_question)
    user_vector = vectorizer.transform([processed_input])
    similarity_scores = cosine_similarity(user_vector, question_vectors)
    best_match_index = similarity_scores.argmax()
    best_score = similarity_scores[0][best_match_index]

    if best_score < 0.2:
        return jsonify({"answer": "Sorry, I could not find a relevant answer. Please try asking differently."})

    return jsonify({"answer": answers[best_match_index]})

if __name__ == "__main__":
    app.run(debug=True)
