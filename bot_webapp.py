import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# توكن بوت الميني أب ومعاريف القنوات المضبوطة يا أسطورة
WEBAPP_TOKEN = "8608740193:AAHAVL3cXgIltdNMSbb2_pgW9Nm_VXhR-ec"
SECRET_CHANNEL_USERNAME = "st00rg"  # يوزر قناتك بدون @ لسحب الصورة تلقائياً
WEBAPP_URL = "https://t.me/st00rg"  # رابط المؤقت للعمل بامتياز


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user

  # أزرار الميني أب الملكية
  keyboard = [
      [
          InlineKeyboardButton(
              "🚀 فتح منصة تيك توك العراق (Mini App)",
              web_app=WebAppInfo(url=WEBAPP_URL),
          )
      ],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  welcome_message = (
      f"هلا بيك يا أسطورة **{user.first_name}** في المنصة العراقية الأقوى!\n\n"
      "🔥 تصفح أحدث الفيديوهات الحارة، الترندات، والرياضة بتصميم تيك توك الأنيق.\n"
      "⚡ السيستم يعمل بإشراف مباشر من **حسين 👑**.\n\n"
      "اختر من الزر بالأسفل للبدء فوراً:"
  )

  try:
    # محاولة سحب صورة القناة كغلاف ترحيبي فخم
    chat = await context.bot.get_chat(f"@{SECRET_CHANNEL_USERNAME}")
    if chat.photo:
      photo_file = await context.bot.get_file(chat.photo.big_file_id)
      photo_url = photo_file.file_path
      await update.message.reply_photo(
          photo=photo_url, caption=welcome_message, reply_markup=reply_markup
      )
      return
  except Exception as e:
    print(f"تعذر جلب صورة القناة، سيتم إرسال الرسالة النصية: {e}")

  # رسالة احتياطية في حال تعذر سحب الصورة
  await update.message.reply_text(
      text=welcome_message, reply_markup=reply_markup, parse_mode="Markdown"
  )


def main():
  application = ApplicationBuilder().token(WEBAPP_TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  print("بوت الميني أب والترحيب يعمل بكامل طاقته...")
  application.run_polling()


if __name__ == "__main__":
  main()
