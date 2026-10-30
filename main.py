import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@test")
ADMIN_ID = os.getenv("ADMIN_ID")

ARMY = ["ضحك","حزن","حب","رعب","اكشن","رياضة","طبخ","موضة","سيارات","العاب","حيوانات","اطفال","موسيقى","رقص","سفر","تعليم","تكنولوجيا","مال","صحة","جمال","ترند"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    status = "✅ محمي" if BOT_TOKEN else "❌ ضيف التوكن بالسكرت"
    return f"{status} | Army: {len(ARMY)} | Channel: {CHANNEL_ID}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
