from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load FAQ data safely
faq_data = []

try:
    faq_path = os.path.join(
        os.path.dirname(__file__),
        "faq_data.json"
    )

    with open(
        faq_path,
        "r",
        encoding="utf-8"
    ) as file:

        faq_data = json.load(file)

except Exception as e:

    print("FAQ Load Error:", str(e))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        user_question = (
            data.get("question", "")
            .lower()
            .strip()
        )

        if not user_question:

            return jsonify({
                "answer":
                "Please enter a question."
            })

        for item in faq_data:

            faq_question = (
                item["question"]
                .lower()
                .strip()
            )

            if (
                user_question in faq_question
                or
                faq_question in user_question
            ):

                return jsonify({
                    "answer":
                    item["answer"]
                })

        return jsonify({
            "answer":
            "Sorry, I could not find a matching answer."
        })

    except Exception as e:

        return jsonify({
            "answer":
            f"Server Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)
