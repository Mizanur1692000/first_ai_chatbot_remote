import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from groq import Groq

# Load environment variable
load_dotenv()

app = Flask(__name__)

# Set up Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.json.get("input", "")

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ valid Groq model
            messages=[{"role": "user", "content": user_input}]
        )
        bot_reply = response.choices[0].message.content.strip()
        return jsonify({"response": bot_reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)