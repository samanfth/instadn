import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# گرفتن توکن از متغیر محیطی
BOT_TOKEN = os.getenv("BOT_TOKEN")

# تابع شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋\nلینک اینستاگرام رو بفرست تا لینک دانلودش رو بدم.")

# تابع پردازش لینک
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com" not in url:
        await update.message.reply_text("⚠️ لطفاً یه لینک معتبر اینستاگرام بفرست.")
        return

    # استفاده از API شخص ثالث برای گرفتن لینک دانلود
    api_url = f"https://ssyoutube.com/api/convert?url={url}"
    try:
        response = requests.get(api_url).json()
        if "url" in response and len(response["url"]) > 0:
            download_url = response["url"][0]["url"]
            await update.message.reply_text(f"✅ لینک دانلود آماده‌ست:\n{download_url}")
        else:
            await update.message.reply_text("❌ نتونستم لینک دانلود پیدا کنم.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")

# اجرای ربات
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    port = int(os.environ.get("PORT", 8080))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=BOT_TOKEN,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
    )

if __name__ == "__main__":
    main()
