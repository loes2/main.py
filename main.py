import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from dotenv import load_dotenv
import os

# تحميل المتغيرات من ملف .env
load_dotenv()

# الحصول على التوكن والمفتاح من البيئة
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# إعداد السجل
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# إعداد OpenAI باستخدام المفتاح من البيئة
openai.api_key = OPENAI_API_KEY

# دالة لمعالجة الأخطاء
async def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="حدث خطأ أثناء معالجة التحديث:", exc_info=context.error)

# أمر /start
async def start(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text("مرحبًا! أنا أليكس، بوت الدردشة والتفاعل.")
    except Exception as e:
        logger.error(f"حدث خطأ في أمر /start: {e}")

# أمر /ask (أسئلة على غرار الذكاء الاصطناعي)
async def ask(update: Update, context: CallbackContext):
    try:
        question = " ".join(context.args)  # دمج الرسالة التي يرسلها المستخدم
        if question:
            response = openai.Completion.create(
                engine="text-davinci-003",  # اختر النموذج الذي ترغب فيه
                prompt=question,
                max_tokens=150
            )
            await update.message.reply_text(response.choices[0].text.strip())
        else:
            await update.message.reply_text("يرجى إرسال سؤال لي للإجابة عليه.")
    except Exception as e:
        logger.error(f"حدث خطأ أثناء معالجة السؤال: {e}")
        await update.message.reply_text("حدث خطأ أثناء معالجة طلبك.")

# الرد على الرسائل
async def reply(update: Update, context: CallbackContext):
    try:
        message = update.message.text
        if message.lower() == "كيف حالك؟":
            await update.message.reply_text("أنا بخير، شكرًا لسؤالك!")
        else:
            await update.message.reply_text("أنا هنا للمساعدة! كيف يمكنني مساعدتك؟")
    except Exception as e:
        logger.error(f"حدث خطأ في الرد على الرسالة: {e}")

# إعداد وتشغيل البوت
async def main():
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # إضافة المعالجات للأوامر
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ask", ask))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
        
        # إضافة معالج الأخطاء العام
        app.add_error_handler(error_handler)

        # بدء تشغيل البوت
        await app.run_polling()
    except Exception as e:
        logger.error(f"حدث خطأ أثناء تشغيل البوت: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
