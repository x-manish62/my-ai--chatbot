from flask import Flask, render_template, request, jsonify
import requests
import json
from pymongo import MongoClient
import os

app = Flask(__name__)

# 👇 1. YAHAN APNI ASLI API KEY DAALEIN
API_KEY = "AIzaSyBvdX_eHWcI7ppuD0uhI98qSiw6ULtHNHA"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"

# 👇 2. Vercel se MongoDB Key aayegi (Database Setup)
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
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": user_msg}]}]
    }
    
    try:
        # Seedha direct API call (Bina kisi library ke)
        response = requests.post(URL, headers=headers, data=json.dumps(data))
        result = response.json()
        
        if "candidates" in result:
            bot_reply = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Database mein save karna (agar Mongo connect hai)
            if db_collection is not None:
                db_collection.insert_one({"user": user_msg, "bot": bot_reply})
                
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"reply": f"API Error: {result.get('error', {}).get('message', 'Unknown Error')}"})
            
    except Exception as e:
        return jsonify({"reply": f"System Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
