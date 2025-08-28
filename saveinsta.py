import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# وب سرور ساده برای Render
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "✅ Bot is running!"

# توکن ربات
BOT_TOKEN = os.getenv("BOT_TOKEN")

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 لینک اینستاگرام رو بفرست تا لینک دانلودش رو آماده کنم.")

# پردازش لینک اینستاگرام
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        await update.message.reply_text("⚠️ لطفاً لینک معتبر بده.")
        return
    try:
        api_url = f"https://ssyoutube.com/api/convert?url={url}"
        r = requests.get(api_url).json()
        if "medias" in r and len(r["medias"]) > 0:
            download_url = r["medias"][0]["url"]
            await update.message.reply_text(f"✅ لینک دانلود آماده‌ست:\n{download_url}")
        else:
            await update.message.reply_text("❌ چیزی پیدا نشد.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")

# اجرای ربات در Thread جدا
def run_telegram_bot():
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
