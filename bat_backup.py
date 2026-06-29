from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8843548872:AAHv8cGi9eRjcR-pZd6MpK6igklM4a2sTCk"

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.video.file_unique_id

    await update.message.reply_text(
        f"شناسه ویدیو:\n{uid}"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.VIDEO, video_handler)
)

print("Bot Started")

app.run_polling()