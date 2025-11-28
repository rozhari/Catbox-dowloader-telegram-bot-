import os
import re
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("Set TELEGRAM_TOKEN environment variable!")

CATBOX_RE = re.compile(r'https?://(?:files\.)?catbox\.moe/\S+')

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Catbox link thaa, file download cheythu tharam!")

def handle(update: Update, context: CallbackContext):
    text = update.message.text or ""
    urls = CATBOX_RE.findall(text)

    if not urls:
        update.message.reply_text("Catbox link kandilla 😅")
        return

    for url in urls:
        msg = update.message.reply_text(f"Downloading: {url} ⏳")

        try:
            r = requests.get(url, stream=True)
            r.raise_for_status()

            filename = url.split("/")[-1]

            with open(filename, "wb") as f:
                f.write(r.content)

            with open(filename, "rb") as f:
                update.message.reply_document(f, filename=filename)

            msg.edit_text("Done ✔️")

            os.remove(filename)

        except Exception as e:
            msg.edit_text(f"Error: {e}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
