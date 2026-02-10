import os
import telebot
import json
import time
import threading
from datetime import datetime
import pytz

from ai import ask_ai, speech_to_text

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

IST = pytz.timezone('Asia/Kolkata')

def load(f):
    try: return json.load(open(f))
    except: return []

def save(f, d):
    json.dump(d, open(f, "w"), indent=2)

reminders = load("reminders.json")

def j(t):
    return f"Jarvis: {t}"

# -------- TEXT MESSAGE --------
@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(m):

    ai = ask_ai(m.text)

    if ai["intent"] == "reminder":

        reminders.append({
            "time": ai["time"],
            "task": ai["task"],
            "chat": m.chat.id
        })

        save("reminders.json", reminders)

        bot.reply_to(m, j(f"Done! {ai['time']} pe yaad dila dunga 👍"))

    else:
        bot.reply_to(m, j(ai["reply"]))


# -------- VOICE MESSAGE --------
@bot.message_handler(content_types=['voice'])
def handle_voice(m):

    file_info = bot.get_file(m.voice.file_id)
    downloaded = bot.download_file(file_info.file_path)

    path = "voice.ogg"
    with open(path, "wb") as f:
        f.write(downloaded)

    text = speech_to_text(path)

    if not text:
        bot.reply_to(m, j("Voice samajh nahi aaya 😅"))
        return

    bot.reply_to(m, j(f"Maine suna: {text}"))

    ai = ask_ai(text)

    if ai["intent"] == "reminder":
        reminders.append({
            "time": ai["time"],
            "task": ai["task"],
            "chat": m.chat.id
        })
        save("reminders.json", reminders)
        bot.send_message(m.chat.id, j(f"Voice reminder set for {ai['time']} 👍"))
    else:
        bot.send_message(m.chat.id, j(ai["reply"]))


# -------- REMINDER ENGINE --------
def loop():
    while True:
        now = datetime.now(IST).strftime("%H:%M")

        for r in reminders[:]:
            if r["time"] == now:
                bot.send_message(
                    r["chat"],
                    j(f"Time ho gaya: {r['task']} 🔔")
                )
                reminders.remove(r)
                save("reminders.json", reminders)

        time.sleep(30)

threading.Thread(target=loop).start()

print("Jarvis AI Started...")
bot.polling()
