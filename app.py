from flask import Flask, render_template, request, jsonify
import json
import os
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(**name**)

# Load FAQ data

BASE_DIR = os.path.dirname(os.path.abspath(**file**))
FAQ_FILE = os.path.join(BASE_DIR, "faq_data.json")

with open(FAQ_FILE, "r", encoding="utf-8") as f:
faq_data = json.load(f)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# Preprocessing

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

vectorizer = TfidfVectorizer(
stop_words="english"
)

question_vectors = vectorizer.fit_transform(
processed_questions
)

@app.route("/")
def home():
return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():

```
data = request.get_json()

question = data.get(
    "question",
    ""
).strip()

if not question:

    return jsonify({
        "answer": "Please enter a question."
    })

processed_input = preprocess_text(
    question
)

user_vector = vectorizer.transform(
    [processed_input]
)

similarity = cosine_similarity(
    user_vector,
    question_vectors
)

best_match = similarity.argmax()

score = similarity[0][best_match]

if score < 0.20:

    return jsonify({
        "answer":
        "Sorry, I couldn't find a matching answer. Try asking about AI, Machine Learning, NLP, Deep Learning, Python or Computer Vision."
    })

return jsonify({
    "answer":
    answers[best_match]
})
```

if **name** == "**main**":
app.run(debug=True)

