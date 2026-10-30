import os
import logging
from flask import Flask, render_template, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# إعدادات المتغيرات البيئية
BOT_TOKEN = os.getenv("BOT_TOKEN", "8608740193:AAHAVL3cXgIltdNMSbb2_pgW9Nm_VXhR-ec")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@st00rg")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# تهيئة الذكاء الاصطناعي
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# واجهة الميني آب
@app.route('/')
def index():
    return render_template('tiktok.html')

# فحص صحة السيرفر
@app.route('/health')
def health():
    return f"✅ الإمبراطورية تعمل بوجبة جيش البوتات | القناة: {CHANNEL_ID}"

# دالة التعامل مع رسائل تليكرام والذكاء الاصطناعي
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_name = update.message.from_user.first_name
    
    # الرد باللهجة العراقية عبر الذكاء الاصطناعي
    prompt = f"""
    أنت نظام الذكاء الاصطناعي المسيطر على "Empire TikTok Hub". 
    رد على المستخدم العراقي {user_name} باللهجة العراقية الطيبة والدافئة، وساعده بطلب.
    رسالة المستخدم: {user_text}
    """
    
    try:
        if GEMINI_API_KEY:
            response = ai_model.generate_content(prompt)
            reply_text = response.text
        else:
            reply_text = "هلا بيك يا حسين، العقل الذكي جاهز بس يحتاج مفتاح الـ API!"
    except Exception as e:
        reply_text = "عفية حسين، صار عندي لود بس دقيقة وأرجعلك!"

    await update.message.reply_text(reply_text)

# بدء تشغيل بوت تليكرام
def run_telegram_bot():
    if not BOT_TOKEN:
        return
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # تشغيل البوت بشكل متزامن
    application.run_polling()

if __name__ == '__main__':
    # ملاحظة: لتشغيل السيرفر والبوت سوية بمحيط واحد، نقدر نربطهم باحترافية
    app.run(host='0.0.0.0', port=8080)
