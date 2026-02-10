import os
import requests
import json

GROQ_KEY = os.environ.get("GROQ_KEY")

# ---------- TEXT AI ----------
def ask_ai(user_text):

    prompt = f"""
You are JARVIS – Anuj ka friendly mentor.
Tone: 4/10 strict, caring + motivating.
Language: Hinglish mix.

Decide intent and reply ONLY in JSON.

If reminder:
{{"intent":"reminder","time":"HH:MM","task":"..."}}

If normal chat:
{{"intent":"chat","reply":"... Hinglish reply ..."}}

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
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4
        }
    )

    try:
        return json.loads(res.json()["choices"][0]["message"]["content"])
    except:
        return {"intent": "chat", "reply": "Thoda clearly bol na Anuj 😊"}
        

# ---------- VOICE TO TEXT ----------
def speech_to_text(file_path):

    with open(file_path, "rb") as f:
        res = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            files={"file": f},
            data={
                "model": "whisper-large-v3",
                "language": "en"
            }
        )

    try:
        return res.json()["text"]
    except:
        return ""
