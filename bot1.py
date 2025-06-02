import os
import aiohttp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Bot Token और Channel ID
BOT_TOKEN = "7960651818:AAFYfETT-JeASRu3_eVCifKc6LbBqZPR-yA"
CHANNEL_ID = "-1002624797462"

# लिंक से फाइल डाउनलोड करने का async फ़ंक्शन
async def download_file(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(filename, 'wb') as f:
                    f.write(await resp.read())
                return True
            return False

# /upload कमांड हैंडलर
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ कृपया एक डायरेक्ट लिंक दें।\nउदाहरण: /upload <लिंक>")
        return

    url = context.args[0]
    filename = "downloaded_file"

    await update.message.reply_text("📥 डाउनलोड किया जा रहा है...")

    if await download_file(url, filename):
        await context.bot.send_document(chat_id=CHANNEL_ID, document=open(filename, 'rb'))
        await update.message.reply_text("✅ सफलतापूर्वक अपलोड हो गया!")
        os.remove(filename)
    else:
        await update.message.reply_text("❌ फ़ाइल डाउनलोड नहीं हो सकी।")

# बॉट को शुरू करने वाला async फ़ंक्शन
async def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("upload", upload))
    print("🤖 बॉट शुरू हो गया है...")
    await app.run_polling()

# अगर Render या Jupyter जैसा environment है
# तो event loop को दोबारा बंद करने की ज़रूरत नहीं होती

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(start_bot())
        loop.run_forever()
    except KeyboardInterrupt:
        print("बॉट बंद कर दिया गया।")
    
