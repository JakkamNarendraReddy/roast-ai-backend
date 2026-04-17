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
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = response.json()

    reply = result["choices"][0]["message"]["content"]

    return jsonify({
        "reply": reply
    })
