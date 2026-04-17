from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/roast", methods=["POST"])
def roast():
    try:
        data = request.json
        prompt = data["prompt"]

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        result = response.json()

        # 🔥 DEBUG LINE (IMPORTANT)
        print(result)

        # ❌ If API failed
        if "choices" not in result:
            return jsonify({
                "reply": "API error: " + str(result)
            })

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "reply": "Server error: " + str(e)
        })
