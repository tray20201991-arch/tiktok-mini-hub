import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# توكن بوت النشر ومعاريف القنوات المحدثة يا أسطورة
PUBLISHER_TOKEN = "8093135920:AAGUUS6k6VPTg0RODMP27FSpI0SdMHquQ4U"
SECRET_CHANNEL = "@st00rg"  # قناتك السرية المصدر للفيديوهات
DESTINATION_CHANNEL = "@your_destination_channel"  # قناتك العامة النهائية

# ذاكرة مانعة للتكرار الجذري
processed_ids = set()


async def fetch_and_boost_trending(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  message = update.channel_post or update.message
  if not message:
    return

  chat_username = message.chat.username
  if chat_username and f"@{chat_username.lower()}" == SECRET_CHANNEL.lower():
    msg_id = message.message_id

    # إذا الفيديو منشور مسبقاً، عبره فوراً بدون أي تأخير لمنع التكرار
    if msg_id in processed_ids:
      return

    caption = message.caption or ""

    # تصنيف الفئات السريعة بلمسة محترف وفيدوهات تفاعلية صاعدة
    category_hashtag = "#ترند_حارق #اكسبلور"
    if any(w in caption for w in ["كرة", "رياضة", "مباريات", "دوري", "هدف"]):
      category_hashtag = "#رياضة #مباريات_حصرية"
    elif any(w in caption for w in ["كوميديا", "ضحك", "مفاجأة", "فصلة"]):
      category_hashtag = "#كوميديا #تسلية_عراقية"
    elif any(w in caption for w in ["سيارات", "تعديل", "محرك", "حلبة"]):
      category_hashtag = "#سيارات #تعديل_موتورات"

    # تنسيق الوصف مع بصمتك الملكية وحقوقك
    new_caption = (
        f"{caption}\n\n{category_hashtag}\n🔥 [فيديو صاعد ومكسب]\n📌 ID: #{msg_id}"
        f" | إشراف: حسين 👑"
    )

    try:
      # نشر فوري وسريع للفيديو الحار بدون تكرار
      await context.bot.copy_message(
          chat_id=DESTINATION_CHANNEL,
          from_chat_id=message.chat.id,
          message_id=msg_id,
          caption=new_caption,
      )

      processed_ids.add(msg_id)
      print(
          f"تم التقاط ونشر الفيديو الحار (ID: {msg_id}) وتوجيهه للقناة بنجاح!"
      )

    except Exception as e:
      print(f"خطأ في معالجة ونشر الفيديو الساخن: {e}")


def main():
  application = ApplicationBuilder().token(PUBLISHER_TOKEN).build()
  application.add_handler(
      MessageHandler(
          filters.Chat(username=SECRET_CHANNEL), fetch_and_boost_trending
      )
  )
  print("بوت الفلترة السريعة والترندات يعمل بكامل طاقته...")
  application.run_polling()


if __name__ == "__main__":
  main()
