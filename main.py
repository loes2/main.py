import logging
import random
import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# إعداد التوكن (ضع توكن البوت هنا)
TOKEN = "7838191538:AAHm79xzV1IlEu5NI-L25majcR_o1EGS49Y"

# قائمة ردود عشوائية
random_replies = ["مرحبا!", "كيف حالك؟", "ماذا تفعل؟", "أنا هنا للمساعدة!", "هل تحتاج إلى شيء؟"]

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

# أمر /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("مرحبًا! أنا أليكس، بوت الدردشة والتفاعل.")

# أمر /truthordare (لعبة كت أو رواية)
async def truth_or_dare_game(update: Update, context: CallbackContext):
    question = random.choice(truth_or_dare)
    await update.message.reply_text(f"🎲 {question}")

# الرد التلقائي على الرسائل
async def reply_randomly(update: Update, context: CallbackContext):
    if update.message.text:
        response = random.choice(random_replies)
        await update.message.reply_text(response)

# أمر /mute (كتم عضو)
async def mute(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("يرجى تحديد المستخدم @username")
        return
    user = context.args[0]
    await update.message.chat.restrict_member(user, ChatPermissions(can_send_messages=False))
    await update.message.reply_text(f"🚫 تم كتم {user} بنجاح!")

# أمر /unmute (إلغاء كتم عضو)
async def unmute(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("يرجى تحديد المستخدم @username")
        return
    user = context.args[0]
    await update.message.chat.restrict_member(user, ChatPermissions(can_send_messages=True))
    await update.message.reply_text(f"✅ تم إلغاء كتم {user} بنجاح!")

# إعداد البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("truthordare", truth_or_dare_game))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_randomly))

    app.run_polling()

if __name__ == "__main__":
    main()