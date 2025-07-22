# admin_panel.py

import telebot
import threading
import subprocess
import time
from pymongo import MongoClient
from datetime import datetime

# === CONFIGURATION ===
ADMIN_CHAT_IDS = [6355601354, 1529778848]  # Put your admin Telegram chat IDs here
MONGO_URI = "mongodb+srv://rabbisudo:HZ7pcIUYsPx85bnN@cluster0.rxhclog.mongodb.net/"  # Replace with your MongoDB URI
DB_NAME = "bot_manager_db"
COLLECTION_NAME = "user_bots"

BOT_TOKEN = "7573920532:AAFqTqp1LyNxKaftygoNi9eq3oD-LKWl068"  # Replace with your admin bot token

bot = telebot.TeleBot(BOT_TOKEN)

# MongoDB Setup
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
bots_col = db[COLLECTION_NAME]

# Dictionary to hold running bot processes {bot_id: subprocess.Popen}
running_bots = {}

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def admin_only(func):
    def wrapper(message, *args, **kwargs):
        if message.chat.id not in ADMIN_CHAT_IDS:
            bot.reply_to(message, "❌ You are not authorized to use this bot.")
            return
        return func(message, *args, **kwargs)
    return wrapper



def start_bot_process(bot_id, token, ws_url, group_id):
    # Start the user bot as subprocess
    if bot_id in running_bots:
        return False, "Bot is already running."

    cmd = [
        "python", "user_bot_template.py",
        bot_id,
        token,
        ws_url,
        group_id
    ]
    proc = subprocess.Popen(cmd)
    running_bots[bot_id] = proc
    # Update DB status
    bots_col.update_one({"bot_id": bot_id}, {"$set": {"status": "running", "start_time": get_current_time()}}, upsert=True)
    return True, "Bot started."


def stop_bot_process(bot_id):
    proc = running_bots.get(bot_id)
    if not proc:
        return False, "Bot is not running."
    proc.terminate()
    proc.wait(timeout=5)
    running_bots.pop(bot_id)
    bots_col.update_one({"bot_id": bot_id}, {"$set": {"status": "stopped"}}, upsert=True)
    return True, "Bot stopped."


def restart_bot_process(bot_id):
    stop_res, stop_msg = stop_bot_process(bot_id)
    if not stop_res:
        return False, f"Cannot restart: {stop_msg}"

    bot_doc = bots_col.find_one({"bot_id": bot_id})
    if not bot_doc:
        return False, "Bot info not found in DB."

    start_res, start_msg = start_bot_process(
        bot_id,
        bot_doc['telegram_token'],
        bot_doc['ws_url'],
        bot_doc['group_id']
    )
    if not start_res:
        return False, f"Restart failed: {start_msg}"

    return True, "Bot restarted."


def get_bot_uptime(bot_id):
    bot_doc = bots_col.find_one({"bot_id": bot_id})
    if not bot_doc:
        return "Unknown"

    if bot_doc.get("status") != "running":
        return "Not running"

    start_time_str = bot_doc.get("start_time")
    if not start_time_str:
        return "Unknown"

    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    delta = now - start_time
    return str(delta).split('.')[0]  # HH:MM:SS


@bot.message_handler(commands=["start", "help"])
@admin_only
def send_welcome(message):
    bot.reply_to(message, (
        "👋 Welcome to Admin Panel Bot!\n\n"
        "Commands:\n"
        "/createbot <bot_id> <telegram_token> <ws_url> <group_id> - Create and start a user bot\n"
        "/stopbot <bot_id> - Stop a running user bot\n"
        "/restartbot <bot_id> - Restart a user bot\n"
        "/listbots - List all bots with status and uptime\n"
        "/botinfo <bot_id> - Show bot info\n"
    ))


@bot.message_handler(commands=["createbot"])
@admin_only
def create_bot_handler(message):
    try:
        args = message.text.split()
        if len(args) != 5:
            bot.reply_to(message, "Usage:\n/createbot <bot_id> <telegram_token> <ws_url> <group_id>")
            return

        bot_id = args[1]
        telegram_token = args[2]
        ws_url = args[3]
        group_id = args[4]

        existing = bots_col.find_one({"bot_id": bot_id})
        if existing:
            bot.reply_to(message, f"Bot with ID '{bot_id}' already exists.")
            return

        bots_col.insert_one({
            "bot_id": bot_id,
            "telegram_token": telegram_token,
            "ws_url": ws_url,
            "group_id": group_id,
            "status": "stopped",
            "start_time": None
        })

        res, msg = start_bot_process(bot_id, telegram_token, ws_url, group_id)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


@bot.message_handler(commands=["stopbot"])
@admin_only
def stop_bot_handler(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Usage:\n/stopbot <bot_id>")
            return

        bot_id = args[1]
        res, msg = stop_bot_process(bot_id)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


@bot.message_handler(commands=["restartbot"])
@admin_only
def restart_bot_handler(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Usage:\n/restartbot <bot_id>")
            return

        bot_id = args[1]
        res, msg = restart_bot_process(bot_id)
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


@bot.message_handler(commands=["listbots"])
@admin_only
def list_bots_handler(message):
    try:
        bots = list(bots_col.find())
        if not bots:
            bot.reply_to(message, "No bots found.")
            return

        lines = []
        for b in bots:
            uptime = get_bot_uptime(b['bot_id'])
            lines.append(f"• {b['bot_id']} — Status: {b.get('status', 'unknown')} — Uptime: {uptime}")

        bot.reply_to(message, "\n".join(lines))
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")


@bot.message_handler(commands=["botinfo"])
@admin_only
def bot_info_handler(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Usage:\n/botinfo <bot_id>")
            return

        bot_id = args[1]
        b = bots_col.find_one({"bot_id": bot_id})
        if not b:
            bot.reply_to(message, "Bot not found.")
            return

        uptime = get_bot_uptime(bot_id)

        info = (
            f"Bot ID: {b['bot_id']}\n"
            f"Status: {b.get('status', 'unknown')}\n"
            f"Uptime: {uptime}\n"
            f"Group ID: {b.get('group_id', 'N/A')}\n"
            f"WebSocket URL: {b.get('ws_url', 'N/A')}\n"
        )
        bot.reply_to(message, info)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

def restore_running_bots():
    print("🔁 Restoring previously running bots from MongoDB...")
    bots = bots_col.find({"status": "running"})
    for bot_doc in bots:
        bot_id = bot_doc["bot_id"]
        token = bot_doc["telegram_token"]
        ws_url = bot_doc["ws_url"]
        group_id = bot_doc["group_id"]

        res, msg = start_bot_process(bot_id, token, ws_url, group_id)
        print(f"▶️ [{bot_id}] {msg}")


if __name__ == "__main__":
    print("🚀 Starting Admin Panel Bot...")
    restore_running_bots()
    bot.infinity_polling()
