import asyncio
import logging
import random
from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)

# إعداد التوكن (ضع توكن البوت هنا)
TOKEN = "7838191538:AAHm79xzV1IlEu5NI-L25majcR_o1EGS49Y"

# قائمة ردود عشوائية
random_replies = [
    "مرحبا!",
    "كيف حالك؟",
    "ماذا تفعل؟",
    "أنا هنا للمساعدة!",
    "هل تحتاج إلى شيء؟"
]

# قائمة أسئلة لعبة "كت أو رواية"
truth_or_dare = [
    "هل سبق لك أن كذبت على شخص مهم؟",
    "ما هو أسوأ سر تخفيه؟",
    "تحدي: ارسل رسالة صوتية تغني فيها!",
    "حقيقة: من هو أقرب شخص إلى قلبك؟"
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

# أمر /truthordare (لعبة كت أو رواية)
async def truth_or_dare_game(update: Update, context: CallbackContext):
    try:
        question = random.choice(truth_or_dare)
        await update.message.reply_text(f"🎲 {question}")
    except Exception as e:
        logger.error(f"حدث خطأ في لعبة كت أو رواية: {e}")

# الرد التلقائي على الرسائل
async def reply_randomly(update: Update, context: CallbackContext):
    try:
        if update.message.text:
            response = random.choice(random_replies)
            await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"حدث خطأ في الرد العشوائي: {e}")

# أمر /mute (كتم عضو)
async def mute(update: Update, context: CallbackContext):
    try:
        if not context.args:
            await update.message.reply_text("يرجى تحديد المستخدم @username")
            return
        user = context.args[0]
        await update.message.chat.restrict_member(user, ChatPermissions(can_send_messages=False))
        await update.message.reply_text(f"🚫 تم كتم {user} بنجاح!")
    except Exception as e:
        logger.error(f"حدث خطأ في كتم المستخدم: {e}")
        await update.message.reply_text("حدث خطأ أثناء محاولة كتم العضو.")

# أمر /unmute (إلغاء كتم عضو)
async def unmute(update: Update, context: CallbackContext):
    try:
        if not context.args:
            await update.message.reply_text("يرجى تحديد المستخدم @username")
            return
        user = context.args[0]
        await update.message.chat.restrict_member(user, ChatPermissions(can_send_messages=True))
        await update.message.reply_text(f"✅ تم إلغاء كتم {user} بنجاح!")
    except Exception as e:
        logger.error(f"حدث خطأ في إلغاء كتم المستخدم: {e}")
        await update.message.reply_text("حدث خطأ أثناء محاولة إلغاء كتم العضو.")

# إعداد وتشغيل البوت
async def main():
    try:
        app = Application.builder().token(TOKEN).build()

        # إضافة المعالجات للأوامر
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("truthordare", truth_or_dare_game))
        app.add_handler(CommandHandler("mute", mute))
        app.add_handler(CommandHandler("unmute", unmute))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_randomly))
        
        # إضافة معالج الأخطاء العام
        app.add_error_handler(error_handler)

        # بدء تشغيل البوت
        await app.run_polling()
    except Exception as e:
        logger.error(f"حدث خطأ أثناء تشغيل البوت: {e}")

if __name__ == "__main__":
    asyncio.run(main())
