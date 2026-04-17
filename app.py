from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/")
def home():
    return "Backend running 🚀"

@app.route("/roast", methods=["POST"])
def roast():
    try:
        data = request.json
        prompt = data["prompt"]

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

        response = requests.post(
            url,
            json={
                "contents": [
                    {
                        "parts": [{"text": f"Roast this person brutally but funny:\n{prompt}"}]
                    }
                ]
            }
        )

        result = response.json()
        print(result)

        if "candidates" not in result:
            return jsonify({"reply": "API error: " + str(result)})

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Server error: " + str(e)})
