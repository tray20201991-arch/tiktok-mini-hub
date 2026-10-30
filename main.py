import os
from flask import Flask, render_template
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
APP_URL = os.environ.get("APP_URL", "")

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN, threaded=False) if TOKEN else None

@app.route('/')
def home():
    return "Bot is Running ✅ - /app/tiktok"

@app.route('/app/tiktok')
def tiktok_app():
    return render_template('tiktok.html')

@bot.message_handler(commands=['start'])
def start(message):
    if not bot:
        return
    markup = InlineKeyboardMarkup()
    if APP_URL:
        markup.add(InlineKeyboardButton(text="🎵 افتح تيك توك", web_app=WebAppInfo(url=APP_URL)))
        bot.send_message(message.chat.id, "اهلا بيك! دوس الزر 👇", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "البوت شغال ✅")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    if bot:
        bot.infinity_polling()

if __name__ == '__main__':
    Thread(target=run_flask).start()
    run_bot()
