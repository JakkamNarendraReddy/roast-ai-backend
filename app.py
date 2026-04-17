from flask_cors import CORS
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
CORS(app)

import os
API_KEY = os.getenv("API_KEY")

@app.route("/roast", methods=["POST"])
def roast():
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
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    result = response.json()

    return jsonify({
        "result": result["choices"][0]["message"]["content"]
    })

app.run(host="0.0.0.0", port=10000)
