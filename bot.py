import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, 
    ConversationHandler, CallbackContext, filters
)
from addmovie import start_add_movie, movie_name_handler, file_id_handler, file_size_handler, file_name_handler, cancel, MOVIE_NAME, FILE_ID, FILE_SIZE, FILE_NAME
from removemovie import remove_movie
from getfile import file_info
from listmovies import list_movies
from loadmovies import load_movies
from help import help_command
from deletemessages import delete_message_later
from movierequest import handle_movie_request
from sendmovie import send_movie

# ✅ Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))  # Default port 8080
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# ✅ Debugging: Print safe environment checks
print(f"✅ BOT_TOKEN Loaded: {'Yes' if BOT_TOKEN else 'No'}")
print(f"✅ PORT: {PORT}")
print(f"✅ GOOGLE CREDENTIALS Loaded: {'Yes' if GOOGLE_CREDENTIALS else 'No'}")

if not BOT_TOKEN:
    raise ValueError("❌ ERROR: BOT_TOKEN is missing! Set it in your environment variables.")
if not GOOGLE_CREDENTIALS:
    print("⚠️ WARNING: GOOGLE_APPLICATION_CREDENTIALS is missing. Google Sheets features may not work.")

# ✅ Flask app for keeping the bot alive
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Bot Status</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #121212;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            }
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .loader {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: conic-gradient(
                    red, yellow, lime, cyan, blue, magenta, red
                );
                animation: spin 1s linear infinite;
            }
            .text {
                font-size: 1.5em;
                margin-top: 20px;
                animation: pulse 1.5s infinite alternate;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes pulse {
                0% { opacity: 0.5; }
                100% { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="loader"></div>
            <h2 class="text">Bot is Running...</h2>
        </div>
    </body>
    </html>
    """

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# ✅ Debug Handler: Logs every received message
async def debug_message(update: Update, context: CallbackContext):
    if update.message:
        print(f"📩 Received message: {update.message.text}")

async def main():
    # ✅ Start Flask server in a background thread
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, run_flask)

    # ✅ Initialize Telegram bot
    tg_app = Application.builder().token(BOT_TOKEN).build()

    # ✅ Debugging Handler (Check if bot is receiving messages)
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, debug_message))

    # ✅ Command Handlers
    tg_app.add_handler(CommandHandler("start", help_command))
    tg_app.add_handler(CommandHandler("help", help_command))
    tg_app.add_handler(MessageHandler(filters.Document.ALL, file_info))
    tg_app.add_handler(CommandHandler("removemovie", remove_movie))
    tg_app.add_handler(CommandHandler("listmovies", list_movies))

    # ✅ Conversation Handler for adding movies
    tg_app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("addmovie", start_add_movie)],
        states={
            MOVIE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, movie_name_handler)],
            FILE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, file_id_handler)],
            FILE_SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, file_size_handler)],
            FILE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, file_name_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    ))

    # ✅ Message Handlers
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_request))
    tg_app.add_handler(CallbackQueryHandler(send_movie))

    print("🚀 Movie Bot is running...")
    await tg_app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
