import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# =====================
# KEYS (abhi empty rahenge)
# =====================
TELEGRAM_TOKEN = "8632052379:AAH95t70Ib3AHuZnQCQdISYFf0RmLVXpP0Y"
GEMINI_API_KEY = "AQ.Ab8RN6LOR2a3K7QWLxoUzUM3kFl0jPNXjqh3u3odlHjL4Vzgeg"


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

WEBSITE_URL = "https://peppy-conkies-877b54.netlify.app"


# =====================
# WEBSITE READ
# =====================

def get_website_text():
    try:
        r = requests.get(WEBSITE_URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.extract()

        return soup.get_text(separator="\n")[:6000]
    except:
        return "Website not accessible"


# =====================
# GEMINI RESPONSE
# =====================

def ask_ai(user_message, website_text):
    prompt = f"""
You are a portfolio assistant bot.

Services:
- App Development
- Web Development
- Video Editing
- Document Editing

RULES:
- Only use website data
- If service not found, politely say not available
- Guide user to contact owner

WEBSITE:
{website_text}

USER:
{user_message}
"""

    response = model.generate_content(prompt)
    return response.text


# =====================
# TELEGRAM HANDLER
# =====================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    website_data = get_website_text()
    reply = ask_ai(text, website_data)

    await update.message.reply_text(reply)


# =====================
# BOT START
# =====================

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot running...")
app.run_polling()
