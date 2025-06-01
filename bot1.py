import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8065762603:AAGnyLy003YWFrkiQrAeyynQsl44PrftPJA")
CHANNEL_ID = os.getenv("-1002624797462")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    try:
        response = requests.get(url)
        filename = url.split('/')[-1].split('?')[0]
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        await context.bot.send_document(chat_id=int(CHANNEL_ID), document=open(filename, 'rb'), caption=f"Uploaded from: {url}")
        os.remove(filename)
        await update.message.reply_text("✅ File uploaded to channel.")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling()
