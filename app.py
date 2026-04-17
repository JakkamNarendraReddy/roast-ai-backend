from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Get API key from Render environment
API_KEY = os.getenv("GEMINI_API_KEY")


@app.route("/")
def home():
    return "🔥 Roast AI Backend Running"


@app.route("/roast", methods=["POST"])
def roast():
    try:
        data = request.get_json()

        if not data or "prompt" not in data:
            return jsonify({
                "reply": "❌ Invalid request. Send JSON with 'prompt'"
            })

        prompt = data["prompt"]

        # ✅ NEW Gemini API (v1)
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": API_KEY
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"Roast this person brutally but funny:\n{prompt}"
                            }
                        ]
                    }
                ]
            }
        )

        result = response.json()
        print(result)  # Debug logs (important)

        # ❌ Handle API errors
        if "candidates" not in result:
            return jsonify({
                "reply": "API error: " + str(result)
            })

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "reply": "Server error: " + str(e)
        })


# ✅ Required for Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
