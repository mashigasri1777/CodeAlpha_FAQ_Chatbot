from flask import Flask, render_template, request, jsonify
import json
import os
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(**name**)

faq_data = []

try:
base_dir = os.path.dirname(os.path.abspath(**file**))
faq_path = os.path.join(base_dir, "faq_data.json")

```
with open(faq_path, "r", encoding="utf-8") as file:
    faq_data = json.load(file)
```

except Exception as e:
print("FAQ Loading Error:", e)

questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

def preprocess_text(text):
text = text.lower()
text = text.translate(str.maketrans('', '', string.punctuation))
return text

if questions:
processed_questions = [
preprocess_text(q)
for q in questions
]

```
vectorizer = TfidfVectorizer(stop_words="english")

question_vectors = vectorizer.fit_transform(
    processed_questions
)
```

else:
vectorizer = None
question_vectors = None

@app.route("/")
def home():
return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():

```
if not vectorizer:
    return jsonify({
        "answer":
        "FAQ database could not be loaded. Check faq_data.json and redeploy."
    })

data = request.get_json()

user_question = data.get(
    "question",
    ""
).strip()

if not user_question:
    return jsonify({
        "answer":
        "Please enter a question."
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
        "Sorry, I couldn't find a relevant answer. Try asking about AI, Machine Learning, NLP, Deep Learning, Python, Neural Networks, Data Science, or Computer Vision."
    })

return jsonify({
    "answer":
    answers[best_match_index]
})
```

if **name** == "**main**":
app.run(debug=True)

