import telebot
import json
import time
import threading
from datetime import datetime
import pytz
import re

TOKEN = "7943836044:AAGwCmRdBeGb7wzwJmKjNUx104d7eFquufM"
bot = telebot.TeleBot(TOKEN)

IST = pytz.timezone('Asia/Kolkata')

def load(f):
    try:
        return json.load(open(f))
    except:
        return []

def save(f,d):
    json.dump(d, open(f,"w"), indent=2)

reminders = load("reminders.json")

# -------- Personality --------
def p(t):
    return f"Purohitji: {t}"

# -------- NLP TIME EXTRACT --------
def get_time(text):
    match = re.findall(r"\d{1,2}[:.]\d{2}", text)
    if match:
        return match[0].replace(".",":")
    return None

# -------- MAIN HANDLER --------
@bot.message_handler(func=lambda m: True)
def talk(m):
    text = m.text.lower()

    # REMINDER INTENT
    if "remind" in text:

        t = get_time(text)

        if not t:
            bot.reply_to(m, p("Tell time clearly like 19:30"))
            return

        task = text.split(t)[-1]

        reminders.append({
            "time": t,
            "task": task,
            "chat": m.chat.id
        })

        save("reminders.json", reminders)

        bot.reply_to(m,
        p(f"Noted for {t}. Excuses will not be accepted."))

    # NORMAL CHAT
    else:
        bot.reply_to(m,
        p("Speak your command clearly Anuj. I am listening."))

# -------- REMINDER ENGINE --------
def loop():
    while True:
        now = datetime.now(IST).strftime("%H:%M")

        for r in reminders:
            if r["time"] == now:
                bot.send_message(r["chat"],
                p(f"TIME TO ACT: {r['task']}"))

                reminders.remove(r)
                save("reminders.json", reminders)

        time.sleep(30)

threading.Thread(target=loop).start()

bot.polling()
