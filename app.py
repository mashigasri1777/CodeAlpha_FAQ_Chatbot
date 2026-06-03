from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is working!"

@app.route("/ask", methods=["POST"])
def ask():
    return jsonify({
        "answer": "Backend is working correctly."
    })

if __name__ == "__main__":
    app.run(debug=True)
