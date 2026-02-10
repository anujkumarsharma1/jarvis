import telebot
import json
import time
import threading
from datetime import datetime

TOKEN = "7943836044:AAGwCmRdBeGb7wzwJmKjNUx104d7eFquufM"    
bot = telebot.TeleBot(TOKEN)

# -------- Memory Functions --------
def load(file):
    try:
        return json.load(open(file))
    except:
        return []

def save(file, data):
    json.dump(data, open(file, "w"), indent=2)

reminders = load("reminders.json")
journal   = load("memory.json")

# -------- Personality Layer --------
def p(text):
    return f"Purohitji: {text}"

# -------- Commands --------

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
    p("I am Purohitji. Discipline is the only religion here."))

# ----- Add Reminder -----
@bot.message_handler(func=lambda m: "remind me at" in m.text.lower())
def add(m):
    try:
        txt = m.text.lower().split("remind me at")[1].strip()
        time_part = txt[:5]
        task = txt[6:]

        reminders.append({
            "time": time_part,
            "task": task,
            "chat": m.chat.id
        })

        save("reminders.json", reminders)

        bot.send_message(m.chat.id,
        p(f"Noted for {time_part}. Excuses will not be accepted."))

    except:
        bot.send_message(m.chat.id,
        p("Format: remind me at 20:00: task"))

# ----- Report Logging -----
@bot.message_handler(func=lambda m: m.text.lower().startswith("report"))
def report(m):
    journal.append({
        "date": str(datetime.now()),
        "text": m.text
    })

    save("memory.json", journal)

    bot.send_message(m.chat.id,
    p("Recorded. I will judge you at night."))

# ----- Progress -----
@bot.message_handler(func=lambda m: "progress" in m.text.lower())
def prog(m):
    last = journal[-5:]
    msg = "Recent honesty:\n"
    for r in last:
        msg += r["text"] + "\n"

    bot.send_message(m.chat.id, p(msg))

# -------- Reminder Engine --------
def loop():
    while True:
        now = datetime.now().strftime("%H:%M")

        for r in reminders:
            if r["time"] == now:
                bot.send_message(r["chat"],
                p(f"TIME TO ACT: {r['task']}"))

        time.sleep(40)

threading.Thread(target=loop).start()

bot.polling()
