@app.route("/roast", methods=["POST"])
def roast():
    try:
        data = request.json
        prompt = data["prompt"]

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
        )

        result = response.json()
        print(result)

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
