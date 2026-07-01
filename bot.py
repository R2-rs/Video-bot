from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

DB_PATH = r"D:\VideoBot\videos.db"

import sqlite3

TOKEN = "8843548872:AAHv8cGi9eRjcR-pZd6MpK6igklM4a2sTCk"

pending_name = None


# =========================
# Database Functions
# =========================

def save_video(file_unique_id, name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO videos (file_unique_id, name) VALUES (?, ?)",
        (file_unique_id, name),
    )

    conn.commit()
    conn.close()


def get_video_name(file_unique_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM videos WHERE file_unique_id = ?",
        (file_unique_id,),
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def get_all_videos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM videos ORDER BY name")

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_video(name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM videos WHERE name = ?",
        (name,),
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted


def count_videos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM videos")

    total = cursor.fetchone()[0]

    conn.close()

    return total

def video_exists(file_unique_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM videos WHERE file_unique_id = ?",
        (file_unique_id,),
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None

# =========================
# Commands
# =========================

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pending_name

    if len(context.args) == 0:
        await update.message.reply_text(
            "مثال:\n/add فیلم آموزشی 1"
        )
        return

    pending_name = " ".join(context.args)

    await update.message.reply_text(
        f"نام ذخیره شد:\n{pending_name}\n\nحالا ویدیو را ارسال کن."
    )


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    videos = get_all_videos()

    if not videos:
        await update.message.reply_text(
            "هیچ ویدیویی ثبت نشده است."
        )
        return

    text = "📚 لیست ویدیوها:\n\n"

    for i, row in enumerate(videos, start=1):
        text += f"{i}. {row[0]}\n"

    await update.message.reply_text(text)


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "مثال:\n/delete فیلم آموزشی 1"
        )
        return

    name = " ".join(context.args)

    deleted = delete_video(name)

    if deleted:
        await update.message.reply_text(
            f"🗑 حذف شد:\n{name}"
        )
    else:
        await update.message.reply_text(
            "چنین ویدیویی پیدا نشد."
        )


async def count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total = count_videos()

    await update.message.reply_text(
        f"📊 تعداد ویدیوها: {total}"
    )


# =========================
# Video Handler
# =========================

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global pending_name

    uid = update.message.video.file_unique_id

    # حالت ثبت
    if pending_name:

        if video_exists(uid):
            await update.message.reply_text(
            "⚠️ این ویدیو قبلاً در دیتابیس ثبت شده است."
            )

            pending_name = None
            return

        save_video(uid, pending_name)

        await update.message.reply_text(
        f"✅ ذخیره شد:\n{pending_name}"
        )

        pending_name = None
        return

    # حالت جستجو
    name = get_video_name(uid)

    if name:
        await update.message.reply_text(
            f"<code>/arise {name}</code>\n\n<code>{name}</code>",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            "❌ این ویدیو در دیتابیس ثبت نشده است."
        )


# =========================
# App
# =========================

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("add", add_command))
app.add_handler(CommandHandler("list", list_command))
app.add_handler(CommandHandler("delete", delete_command))
app.add_handler(CommandHandler("count", count_command))

app.add_handler(
    MessageHandler(filters.VIDEO, video_handler)
)

print("Bot Started")

app.run_polling()