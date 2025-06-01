import os
import asyncio
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot token and Channel ID
BOT_TOKEN = "7960651818:AAFYfETT-JeASRu3_eVCifKc6LbBqZPR-yA"
CHANNEL_ID = "-1002624797462"

# Download the file from the given URL
async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(filename, 'wb') as f:
                    f.write(await resp.read())
                return True
            return False

# Command handler: /upload <direct_link>
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a direct link.\n\nFormat: /upload <link>")
        return

    url = context.args[0]
    filename = "downloaded_file"

    await update.message.reply_text("📥 Downloading...")

    if await download_file(url, filename):
        await context.bot.send_document(chat_id=CHANNEL_ID, document=open(filename, 'rb'))
        await update.message.reply_text("✅ Uploaded successfully!")
        os.remove(filename)
    else:
        await update.message.reply_text("❌ Failed to download the file.")

# Main function to start the bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("upload", upload))
    await app.run_polling()

# Entry point
if __name__ == '__main__':
     import asyncio

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        
