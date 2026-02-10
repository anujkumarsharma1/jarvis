import os
import requests
import json

GROQ_KEY = os.environ.get("GROQ_KEY")

def ask_ai(user_text, history=[]):

    prompt = f"""
You are Purohitji – strict mentor for Anuj.

Decide intent from message and respond in JSON only.

If reminder:
{{"intent":"reminder","time":"HH:MM","task":"..."}}

If normal chat:
{{"intent":"chat","reply":"..."}}

User: {user_text}
"""

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role":"user","content":prompt}],
            "temperature":0.3
        }
    )

    try:
        return json.loads(res.json()["choices"][0]["message"]["content"])
    except:
        return {"intent":"chat","reply":"I did not understand."}
