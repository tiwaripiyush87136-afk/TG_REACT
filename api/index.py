import os
import telebot
import requests
import random
import time
from flask import Flask, request

# --- ENV ----
MAIN_BOT_TOKEN = os.getenv("MAIN_BOT_TOKEN")
OTHER_TOKENS_STR = os.getenv("OTHER_BOT_TOKENS", "")

BOT_TOKENS = [MAIN_BOT_TOKEN]
if OTHER_TOKENS_STR:
    BOT_TOKENS.extend([t.strip() for t in OTHER_TOKENS_STR.split(",") if t.strip()])

SELECTED_EMOJIS = [
    "⭐", "❤️‍🔥", "🗿", "💘", "😇", "🥰", "🌚", 
    "😘", "🔥", "😍", "😈", "⚡", "😎", "🙈", "👀", 
    "💋", "🙊", "🎉", "💯", "🏆"
]

bot = telebot.TeleBot(MAIN_BOT_TOKEN, threaded=False)
app = Flask(__name__)

def send_reaction(token, chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{token}/setMessageReaction"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}],
        "is_big": True
    }
    try:
        
        
        requests.post(url, json=payload, timeout=5)
    except:
        pass


@app.route('/api/index', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Error', 400


@bot.channel_post_handler(content_types=['text', 'photo', 'audio', 'video', 'document', 'sticker', 'video_note', 'voice', 'location', 'contact', 'animation'])
def handle_channel_post(message):
    chat_id = message.chat.id
    message_id = message.message_id
    
    
    for token in BOT_TOKENS:
        random_emoji = random.choice(SELECTED_EMOJIS)
        send_reaction(token, chat_id, message_id, random_emoji)
        
        time.sleep(0.05)

@app.route('/')
def home():
    return "Reaction Api Is active !! ~ AP BOTS | @DEV_PIYUSH | @PYANUJ"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
