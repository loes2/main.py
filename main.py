import logging
import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio

# تحميل المتغيرات من ملف .env
load_dotenv()

# الحصول على التوكن والمفتاح من البيئة
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# إعداد الـ OpenAI
openai.api_key = OPENAI_API_KEY

# إعداد تسجيل الأحداث (Logging)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة الرد على الرسائل الخاصة
async def start(update: Update, context: CallbackContext) -> None:
    # إذا كانت الرسالة من المستخدم الخاص (وليس من مجموعة)
    if update.message.chat.type == 'private':
        await update.message.reply_text("مرحبًا! كيف يمكنني مساعدتك؟")
    else:
        # لا يرد في المجموعات
        pass

# دالة للتفاعل مع OpenAI (اختياري)
async def chat_with_openai(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        user_message = update.message.text

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=user_message,
                max_tokens=150
            )
            await update.message.reply_text(response.choices[0].text.strip())
        except openai.error.OpenAIError as e:
            await update.message.reply_text("عذرًا، حدث خطأ أثناء الاتصال بـ OpenAI.")
            logger.error(f"خطأ أثناء الاتصال بـ OpenAI: {e}")
        except Exception as e:
            await update.message.reply_text("عذرًا، حدث خطأ غير معروف.")
            logger.error(f"خطأ غير معروف: {e}")

# دالة لمعالجة الأخطاء
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'خطأ في التحديث {update} - {context.error}')

# دالة لتشغيل البوت
async def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # إضافة أوامر البوت
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_openai))

    # إضافة دالة للأخطاء
    application.add_error_handler(error)

    # تشغيل البوت
    try:
        await application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"حدث خطأ أثناء تشغيل البوت: {e}")

# دالة أساسية لتشغيل التطبيق
if __name__ == '__main__':
    asyncio.run(main())
