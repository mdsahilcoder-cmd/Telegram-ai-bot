from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import os
TOKEN = os.getenv("8632052379:AAH95t70Ib3AHuZnQCQdISYFf0RmLVXpP0Y")"

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    await update.message.reply_text(
        f"Message mila: {user_message}\nBot ka backend kaam kar raha hai ✅"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, reply))

print("Bot running...")

app.run_polling()
