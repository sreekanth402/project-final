from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/')
def home():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message")
        history = data.get("history", [])

        if not message:
            return jsonify({"error": "Message is required"}), 400

        # Use Gemini model with a friendly instruction
        model = genai.GenerativeModel(
                 model_name="gemini-2.0-flash",
                 system_instruction=(
                    "You are Doc4U, a compassionate healthcare assistant. "
                    "You can understand and respond in the same language as the user — "
                    "for example English, Hindi, Telugu, Tamil, or any language the user speaks. "
                    "Use a friendly, natural tone suitable for WhatsApp messages, with emojis and short paragraphs. "
                    "If the question is about health, give clear, simple advice anyone can understand. "
                    "Always end with a disclaimer: 'Please consult a licensed doctor for personalized medical advice.'"
    )
)


        # Maintain chat history
        chat = model.start_chat(history=history)
        response = chat.send_message(message)

        # Extract text safely
        reply_text = response.text.strip() if response else "Sorry, I couldn’t generate a reply."

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("❌ Server error:", e)
        return jsonify({"error": "Failed to generate response", "details": str(e)}), 500


if __name__ == "__main__":
    print("✅ Flask server running at http://localhost:3000")
    app.run(host="0.0.0.0", port=3000, debug=True)
