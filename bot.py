bc# ~Sαѕυкє

import os
import json
import requests
from datetime import datetime
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

API_BASE = "https://7105.api.greenapi.com"
GREEN_API_INSTANCE = "7105480420"
GREEN_API_TOKEN = "356dfef946cf4c9c948744bca9b2cab3912cfc19c37e4bb1b6"

ADMIN_NUMBER = "916361638776"
DEFAULT_GROUP = "120363425002130781@g.us"

FILE = "reminders.json"

app = Flask(__name__)
scheduler = BackgroundScheduler()
sent = set()

def load():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump({"groups": {}, "reminders": {}}, f)
    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def send(chat, msg):
    url = f"{API_BASE}/waInstance{GREEN_API_INSTANCE}/sendMessage/{GREEN_API_TOKEN}"
    requests.post(url, json={"chatId": chat, "message": msg}, timeout=10)

def startup():
    send(ADMIN_NUMBER + "@c.us", "This bot is ready and working fine ~Sαѕυкє")

def commands(sender, text):
    data = load()
    parts = text.strip().split(" ", 4)

    if text.startswith("!addgroup"):
        if len(parts) < 3:
            return "Use: !addgroup name groupId"
        data["groups"][parts[1]] = parts[2]
        save(data)
        return "Group saved"

    if text.startswith("!groups"):
        if not data["groups"]:
            return "No groups"
        out = "Groups\n\n"
        for g in data["groups"]:
            out += g + " -> " + data["groups"][g] + "\n"
        return out

    if text.startswith("!setgroup"):
        if len(parts) < 5:
            return "Use: !setgroup group Monday 07:00 Message"
        g = parts[1]
        d = parts[2].capitalize()
        t = parts[3]
        m = parts[4]
        if g not in data["groups"]:
            return "Group not found"
        data["reminders"].setdefault(d, []).append({"time": t, "message": m, "group": g})
        save(data)
        return "Saved"

    if text.startswith("!set"):
        if len(parts) < 4:
            return "Use: !set Monday 07:00 Message"
        d = parts[1].capitalize()
        t = parts[2]
        m = parts[3]
        data["reminders"].setdefault(d, []).append({"time": t, "message": m, "group": "__default__"})
        save(data)
        return "Saved"

    if text.startswith("!list"):
        if not data["reminders"]:
            return "No reminders"
        out = "Reminders\n\n"
        for d in data["reminders"]:
            out += d + "\n"
            for r in data["reminders"][d]:
                out += r["time"] + " -> " + r["message"] + " [" + r["group"] + "]\n"
            out += "\n"
        return out

    if text.startswith("!clear"):
        if len(parts) < 2:
            return "Use: !clear Monday"
        d = parts[1].capitalize()
        if d in data["reminders"]:
            del data["reminders"][d]
            save(data)
            return "Cleared"
        else:
            return "Nothing found"

    return None

def inbox():
    url = f"{API_BASE}/waInstance{GREEN_API_INSTANCE}/receiveNotification/{GREEN_API_TOKEN}"
    try:
        res = requests.get(url, timeout=10).json()
    except:
        return
    if not res:
        return

    body = res.get("body", {})
    rid = res.get("receiptId")

    if body.get("typeWebhook") == "incomingMessageReceived":
        sender = body.get("senderData", {}).get("sender", "")
        text = body.get("messageData", {}).get("textMessageData", {}).get("textMessage", "")
        if sender.replace("@c.us", "") == ADMIN_NUMBER:
            reply = commands(sender, text)
            if reply:
                send(sender, reply)

    if rid:
        requests.delete(f"{API_BASE}/waInstance{GREEN_API_INSTANCE}/deleteNotification/{GREEN_API_TOKEN}/{rid}")

def engine():
    now = datetime.now()
    d = now.strftime("%A")
    t = now.strftime("%H:%M")
    key = d + "_" + t
    data = load()

    if d in data["reminders"]:
        for r in data["reminders"][d]:
            if r["time"] == t and key not in sent:
                if r["group"] == "__default__":
                    gid = DEFAULT_GROUP
                else:
                    gid = data["groups"].get(r["group"])
                if gid:
                    send(gid, r["message"])
                sent.add(key)

    inbox()

@app.route("/")
def home():
    return "~Sαѕυкє bot running"

if __name__ == "__main__":
    scheduler.add_job(engine, "interval", seconds=30)
    scheduler.start()
    startup()
    app.run(host="0.0.0.0", port=10000)

# ~Sαѕυкє
