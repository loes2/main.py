import os
import logging
import random
import openai
from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)
from dotenv import load_dotenv

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد التوكن (من ملف .env)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعداد المفتاح API لـ OpenAI
openai.api_key = OPENAI_API_KEY

# قائمة ردود عشوائية
random_replies = [
    "مرحبا!",
    "كيف حالك؟",
    "ماذا تفعل؟",
    "أنا هنا للمساعدة!",
    "هل تحتاج إلى شيء؟"
]

# إعداد السجل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة لمعالجة الأخطاء العامة
async def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(msg="حدث خطأ أثناء معالجة التحديث:", exc_info=context.error)
    # يمكن إرسال رسالة للمستخدم إن رغبت بذلك (اختياري)
    if update and getattr(update, "message", None):
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك.")

# أمر /start
async def start(update: Update, context: CallbackContext):
    try:
        await update.message.reply_text("مرحبًا! أنا أليكس، بوت الدردشة والتفاعل.")
    except Exception as e:
        logger.error(f"حدث خطأ في أمر /start: {e}")

# الرد التلقائي على الرسائل باستخدام GPT-3
async def reply_randomly(update: Update, context: CallbackContext):
    try:
        if update.message.text:
            # إرسال النص إلى OpenAI للحصول على رد ذكي
            response = openai.Completion.create(
                engine="text-davinci-003",  # يمكنك استخدام نموذج GPT-3 آخر إذا أردت
                prompt=update.message.text,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            # إرسال الرد إلى المستخدم
            await update.message.reply_text(response.choices[0].text.strip())
    except Exception as e:
        logger.error(f"حدث خطأ في الرد العشوائي: {e}")

# إعداد وتشغيل البوت
async def main():
    try:
        app = Application.builder().token(TOKEN).build()

        # إضافة المعالجات للأوامر
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_randomly))
        
        # إضافة معالج الأخطاء العام
        app.add_error_handler(error_handler)

        # بدء تشغيل البوت
        await app.run_polling()
    except Exception as e:
        logger.error(f"حدث خطأ أثناء تشغيل البوت: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
