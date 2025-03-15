import asyncio
from flask import Flask
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from addmovie import add_movie
from removemovie import remove_movie
from getfile import file_info
from listmovies import list_movies
from loadmovies import load_movies
from help import help_command
from deletemessages import delete_message_later
from movierequest import handle_movie_request
from sendmovie import send_movie

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

BOT_TOKEN = "7903162641:AAFJkO5g6QzJnxUYwpLcaYUvaIHzC84mxvk"

def main():
    app_thread = Thread(target=run_flask)
    app_thread.start()
    
    tg_app = Application.builder().token(BOT_TOKEN).build()
    tg_app.add_handler(CommandHandler("start", help_command))
    tg_app.add_handler(CommandHandler("help", help_command))
    tg_app.add_handler(CommandHandler("fileinfo", file_info))
    tg_app.add_handler(CommandHandler("addmovie", add_movie))
    tg_app.add_handler(CommandHandler("removemovie", remove_movie))
    tg_app.add_handler(CommandHandler("listmovies", list_movies))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_request))
    tg_app.add_handler(CallbackQueryHandler(send_movie))
    
    print("Bot is running...")
    tg_app.run_polling()

if __name__ == "__main__":
    main()
