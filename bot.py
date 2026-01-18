import requests, json, time, schedule, threading

# ========== CONFIG ==========
API_URL = "https://7105.api.greenapi.com"
ID_INSTANCE = "7105480420"
API_TOKEN = "356dfef946cf4c9c948744bca9b2cab3912cfc19c37e4bb1b6"

ADMIN = "916361638776@c.us"
DATA_FILE = "data.json"


# ========== BASIC ==========
def send_message(chat_id, text):
    url = f"{API_URL}/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    requests.post(url, json={"chatId": chat_id, "message": text})


def load():
    try:
        return json.load(open(DATA_FILE))
    except:
        return {"users": {}, "groups": {}}


def save(data):
    json.dump(data, open(DATA_FILE, "w"), indent=2)


data = load()


# ========== REMINDER SYSTEM ==========
def add_reminder(user, day, time_, msg):
    data["users"].setdefault(user, []).append({
        "day": day, "time": time_, "msg": msg
    })
    save(data)


def clear_day(user, day):
    if user in data["users"]:
        data["users"][user] = [r for r in data["users"][user] if r["day"] != day]
        save(data)


def list_reminders(user):
    if user not in data["users"] or not data["users"][user]:
        return "No reminders set."
    text = "Your reminders:\n"
    for r in data["users"][user]:
        text += f'{r["day"]} {r["time"]} → {r["msg"]}\n'
    return text


# ========== GROUP SYSTEM ==========
def add_group(name, gid):
    data["groups"][name] = gid
    save(data)


def add_group_reminder(group, day, time_, msg):
    data["groups"].setdefault(group+"_rem", []).append({
        "day": day, "time": time_, "msg": msg
    })
    save(data)


# ========== SCHEDULER ==========
def run_scheduler():
    def check():
        now = time.strftime("%A %H:%M")

        # users
        for user in data["users"]:
            for r in data["users"][user]:
                if f'{r["day"]} {r["time"]}' == now:
                    send_message(user, r["msg"])

        # groups
        for g in data["groups"]:
            key = g+"_rem"
            if key in data:
                for r in data[key]:
                    if f'{r["day"]} {r["time"]}' == now:
                        send_message(data["groups"][g], r["msg"])

    schedule.every(1).minutes.do(check)
    while True:
        schedule.run_pending()
        time.sleep(1)


# ========== COMMAND HANDLER ==========
def handle(chat, msg):
    p = msg.split()

    if msg.startswith("!set"):
        add_reminder(chat, p[1], p[2], " ".join(p[3:]))
        send_message(chat, "Reminder set ✅")

    elif msg == "!list":
        send_message(chat, list_reminders(chat))

    elif msg.startswith("!clear"):
        clear_day(chat, p[1])
        send_message(chat, "Cleared ✅")

    elif msg.startswith("!addgroup"):
        add_group(p[1], p[2])
        send_message(chat, "Group added ✅")

    elif msg.startswith("!setgroup"):
        add_group_reminder(p[1], p[2], p[3], " ".join(p[4:]))
        send_message(chat, "Group reminder set ✅")


# ========== START ==========
threading.Thread(target=run_scheduler).start()
send_message(ADMIN, "Reminder bot is running ✅")
