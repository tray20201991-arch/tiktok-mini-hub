import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# توكن بوت الميني أب (الثاني)
WEBAPP_TOKEN = os.getenv("WEBAPP_TOKEN", "حط_توكن_بوت_الميني_اب_هنا")
# رابط الميني أب مالك (مثل Vercel أو الاستضافة اللي راح ترفع عليها الواجهة)
WEBAPP_URL = "https://your-mini-app-url.com"
# معرف قناتك السرية حتى نسحب صورتها تلقائياً
SECRET_CHANNEL = "@your_secret_channel"

# معاريف التواصل الرسمية الخاصة بك
TELEGRAM_USER = "IME44"
INSTAGRAM_USER = "kw8c"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  chat_id = update.effective_chat.id

  # رسالة الترحيب الفخمة
  welcome_text = (
      f"مرحباً بك يا {user.first_name} في عالم التيك توك الحصري 🎬🔥\n\n"
      "أقوى الفيديوهات الترند والحارة، تصفح سريع، أوفلاين، وبأقسام متنوعة.\n\n"
      "👇 اضغط على الزر أدناه لدخول التطبيق واستمتع بالتجربة:"
  )

  # الأزرار المائية الملونة والفخمة
  keyboard = [
      [
          InlineKeyboardButton(
              "🚀 افتح Mini App الملكي", web_app=WebAppInfo(url=WEBAPP_URL)
          )
      ],
      [
          InlineKeyboardButton(
              "📢 تليجرام التواصل", url=f"https://t.me/{TELEGRAM_USER}"
          ),
          InlineKeyboardButton(
              "📸 انستجرام", url=f"https://instagram.com/{INSTAGRAM_USER}"
          ),
      ],
      [
          InlineKeyboardButton(
              "⚠️ الإبلاغ عن مشكلة", url=f"https://t.me/{TELEGRAM_USER}"
          )
      ],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  try:
    # جلب صورة بروفايل القناة السرية تلقائياً
    chat = await context.bot.get_chat(SECRET_CHANNEL)
    photos = await chat.get_profile_photos()

    if photos.total_count > 0:
      file_id = photos.photos[0][-1].file_id
      await context.bot.send_photo(
          chat_id=chat_id,
          photo=file_id,
          caption=welcome_text,
          reply_markup=reply_markup,
      )
    else:
      await context.bot.send_message(
          chat_id=chat_id, text=welcome_text, reply_markup=reply_markup
      )

  except Exception as e:
    print(f"خطأ في سحب صورة القناة: {e}")
    await context.bot.send_message(
        chat_id=chat_id, text=welcome_text, reply_markup=reply_markup
    )


def main():
  application = ApplicationBuilder().token(WEBAPP_TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  print("بوت الميني أب والترحيب يعمل بكفاءة...")
  application.run_polling()


if __name__ == "__main__":
  main()
