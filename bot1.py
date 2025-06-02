import os
import asyncio
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# बॉट टोकन और चैनल आईडी
BOT_TOKEN = "7960651818:AAFYfETT-JeASRu3_eVCifKc6LbBqZPR-yA"
CHANNEL_ID = "-1002624797462"

# फ़ाइल डाउनलोड करने वाला फ़ंक्शन
async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(filename, 'wb') as f:
                    f.write(await resp.read())
                return True
            return False

# /upload कमांड के लिए हैंडलर
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ कृपया एक डायरेक्ट लिंक दें।\nउदाहरण: /upload <लिंक>")
        return

    url = context.args[0]
    filename = "downloaded_file"

    await update.message.reply_text("📥 डाउनलोड किया जा रहा है...")

    if await download_file(url, filename):
        await context.bot.send_document(chat_id=CHANNEL_ID, document=open(filename, 'rb'))
        await update.message.reply_text("✅ सफलतापूर्वक अपलोड कर दिया गया!")
        os.remove(filename)
    else:
        await update.message.reply_text("❌ फ़ाइल डाउनलोड नहीं हो सकी।")

# बॉट शुरू करने का मुख्य फंक्शन
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("upload", upload))
    await app.run_polling()

# मुख्य प्रवेश बिंदु (Render में safe तरीके से asyncio इस्तेमाल किया गया है)
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
