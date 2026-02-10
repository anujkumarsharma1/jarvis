import os
import telebot
import json
import time
import threading
from datetime import datetime
import pytz
from ai import ask_ai

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

IST = pytz.timezone('Asia/Kolkata')

def load(f):
    try: return json.load(open(f))
    except: return []

def save(f,d):
    json.dump(d, open(f,"w"), indent=2)

reminders = load("reminders.json")

def p(t):
    return f"Purohitji: {t}"

@bot.message_handler(func=lambda m: True)
def handle(m):

    ai = ask_ai(m.text)

    # ----- REMINDER INTENT -----
    if ai["intent"] == "reminder":

        reminders.append({
            "time": ai["time"],
            "task": ai["task"],
            "chat": m.chat.id
        })

        save("reminders.json", reminders)

        bot.reply_to(m, p(f"Noted for {ai['time']}. No excuses."))

    # ----- CHAT INTENT -----
    else:
        bot.reply_to(m, p(ai["reply"]))


def loop():
    while True:
        now = datetime.now(IST).strftime("%H:%M")

        for r in reminders[:]:
            if r["time"] == now:
                bot.send_message(
                    r["chat"],
                    p(f"TIME TO ACT: {r['task']}")
                )
                reminders.remove(r)
                save("reminders.json", reminders)

        time.sleep(30)

threading.Thread(target=loop).start()

bot.polling()
