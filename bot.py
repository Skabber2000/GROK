from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)
import requests
import nest_asyncio
import asyncio

# Apply nest_asyncio to allow running an event loop in Colab
nest_asyncio.apply()

# GROK API Configuration
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
MODEL_NAME = "grok-beta"

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Function to get a response from GROK
def get_grok_response(user_message):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": user_message}],
    }
    response = requests.post(GROK_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Command handler for /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your GROK chatbot. Send me a message, and I will respond!")

# Message handler to process user messages
async def chat(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        response = get_grok_response(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

# Main function to start the bot
async def main():
    # Build the bot application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for commands and messages
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Start the bot
    print("Bot is running...")
    await app.run_polling()

# Run the bot using asyncio in Colab
await main()
