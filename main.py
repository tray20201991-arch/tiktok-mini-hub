import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# التوكن يجي من Secrets - مستحيل ينباك!
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel")
ADMIN_ID = os.getenv("ADMIN_ID")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return f"Bot is running! Token protected: {BOT_TOKEN[:5]}..."

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("❌ ضيف BOT_TOKEN بالـ Secrets مال Replit!")
    app.run(host='0.0.0.0', port=8080)
