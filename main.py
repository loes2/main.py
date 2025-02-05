import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai

# تحميل المتغيرات من .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# التحقق من أن المتغيرات تم تحميلها بنجاح
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("🚨 خطأ: لم يتم العثور على TELEGRAM_BOT_TOKEN في البيئة!")
if not OPENAI_API_KEY:
    raise ValueError("🚨 خطأ: لم يتم العثور على OPENAI_API_KEY في البيئة!")

# إعداد OpenAI
openai.api_key = OPENAI_API_KEY

# إعداد نظام التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة لمعالجة الرسائل
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    try:
        # إرسال الطلب إلى OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"⚠️ خطأ أثناء الاتصال بـ OpenAI: {e}")
        reply_text = "عذرًا، حدث خطأ أثناء معالجة طلبك."

    await update.message.reply_text(reply_text)

# دالة لبدء التشغيل
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # إضافة معالج للرسائل
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # تشغيل البوت باستخدام asyncio.run() لمنع مشاكل event loop
    try:
        asyncio.run(application.run_polling())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(application.run_polling())

if __name__ == "__main__":
    main()
