import logging
import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes

# تحميل المتغيرات من ملف .env
load_dotenv()

# الحصول على التوكن والمفتاح من البيئة
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# إعداد OpenAI
openai.api_key = OPENAI_API_KEY

# إعداد تسجيل الأحداث (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة الرد على /start في الخاص فقط
async def start(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        await update.message.reply_text("مرحبًا! كيف يمكنني مساعدتك؟")

# دالة التفاعل مع OpenAI في الخاص فقط
async def chat_with_openai(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        user_message = update.message.text

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            reply_text = response['choices'][0]['message']['content'].strip()
            await update.message.reply_text(reply_text)
        except openai.error.OpenAIError as e:
            await update.message.reply_text("عذرًا، حدث خطأ أثناء الاتصال بـ OpenAI.")
            logger.error(f"خطأ أثناء الاتصال بـ OpenAI: {e}")
        except Exception as e:
            await update.message.reply_text("عذرًا، حدث خطأ غير معروف.")
            logger.error(f"خطأ غير معروف: {e}")

# دالة لمعالجة الأخطاء
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'خطأ في التحديث {update} - {context.error}')

# تشغيل البوت
async def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).context_types(ContextTypes.DEFAULT_TYPE).build()

    # إضافة أوامر البوت
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_openai))

    # إضافة دالة للأخطاء
    application.add_error_handler(error)

    # تشغيل البوت
    logger.info("✅ البوت يعمل الآن...")
    await application.run_polling(drop_pending_updates=True)

# تشغيل البوت إذا كان السكريبت الرئيسي
if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())  # حل مشكلة event loop
    except Exception as e:
        logger.error(f"❌ حدث خطأ أثناء تشغيل البوت: {e}")
