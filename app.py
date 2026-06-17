from flask import Flask, render_template, request, jsonify
from groq import Groq
from pymongo import MongoClient
import os

app = Flask(__name__)

# ==============================
# GROQ API
# ==============================

client_ai = Groq(
    api_key=os.environ.get("GROK_API_KEY")
)

# ==============================
# MONGODB
# ==============================

MONGO_URI = os.environ.get("MONGO_URI")

db_collection = None

if MONGO_URI:

    client = MongoClient(MONGO_URI)

    db = client["ChatbotDB"]

    db_collection = db["chats"]

# ==============================
# HOME PAGE
# ==============================

@app.route('/')

def home():

    return render_template('index.html')

# ==============================
# CHAT API
# ==============================

@app.route('/chat', methods=['POST'])

def chat():

    user_msg = request.json.get("message")

    try:

        # AI RESPONSE

        chat_completion = client_ai.chat.completions.create(

        messages=[
    {
        "role": "system",
        "content": """
You are a friendly AI assistant.

Give short and natural answers.
Do not give long theory.
Reply like a human.
Use simple English.
Keep answers under 4-5 lines unless the user asks for details.

If someone asks who created you, reply:
'I was created and developed by Manish Yadav.'
"""
    },

    {
        "role": "user",
        "content": user_msg
    }
]

            model="llama-3.3-70b-versatile"

        )

        bot_reply = chat_completion.choices[0].message.content

        # DATABASE SAVE

        if db_collection is not None:

            db_collection.insert_one({

                "user": user_msg,

                "bot": bot_reply

            })

        return jsonify({

            "reply": bot_reply

        })

    except Exception as e:

        return jsonify({

            "reply": f"System Error: {str(e)}"

        })

# ==============================
# RUN APP
# ==============================

if __name__ == '__main__':

    app.run(debug=True)
