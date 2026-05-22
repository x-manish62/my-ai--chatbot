from flask import Flask, render_template, request, jsonify
import requests
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env file load karega
load_dotenv()

app = Flask(__name__)

# Gemini API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini configure
genai.configure(api_key=API_KEY)

# Gemini API URL
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# MongoDB
MONGO_URI = os.environ.get("MONGO_URI")

db_collection = None

if MONGO_URI:
    client = MongoClient(MONGO_URI)
    db = client["ChatbotDB"]
    db_collection = db["chats"]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():

    user_msg = request.json.get("message")

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_msg
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(
            URL,
            headers=headers,
            data=json.dumps(data)
        )

        result = response.json()

        if "candidates" in result:

            bot_reply = result["candidates"][0]["content"]["parts"][0]["text"]

            # MongoDB save
            if db_collection is not None:
                db_collection.insert_one({
                    "user": user_msg,
                    "bot": bot_reply
                })

            return jsonify({
                "reply": bot_reply
            })

        else:

            return jsonify({
                "reply": f"API Error: {result.get('error', {}).get('message', 'Unknown Error')}"
            })

    except Exception as e:

        return jsonify({
            "reply": f"System Error: {str(e)}"
        })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )