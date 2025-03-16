import os
import json
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, filters
from flask import Flask
from threading import Thread

# Load Google Sheets API Credentials from Environment Variable
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))
creds = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
client = gspread.authorize(creds)

# Open Google Sheet
SHEET_NAME = "MoviesDatabase"
sheet = client.open(SHEET_NAME).sheet1

def load_movies():
    """Load movies from Google Sheet."""
    movies = {}
    data = sheet.get_all_values()
    for row in data[1:]:
        if len(row) >= 4:
            movie_name, file_id, file_size, file_name = row[:4]
            movies[movie_name] = {
                "file_id": file_id,
                "file_size": file_size,
                "file_name": file_name
            }
    return movies

def save_movies(movies):
    """Save movies to Google Sheet."""
    sheet.clear()
    sheet.append_row(["Movie Name", "File ID", "File Size", "File Name"])
    for movie, details in movies.items():
        sheet.append_row([movie, details["file_id"], details["file_size"], details["file_name"]])

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "<h2>Bot is Running...</h2>"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Telegram Bot Setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 7743703095
MOVIE_NAME, FILE_ID, FILE_SIZE, FILE_NAME = range(4)

def main():
    app_thread = Thread(target=run_flask)
    app_thread.start()
    
    tg_app = Application.builder().token(BOT_TOKEN).build()
    
    from addmovie import start_add_movie, movie_name_handler, file_id_handler, file_size_handler, file_name_handler, cancel
    from removemovie import remove_movie
    from getfile import file_info
    from listmovies import list_movies
    from movierequest import handle_movie_request
    from sendmovie import send_movie
    from help import help_command
    from deletemessages import delete_message_later

    tg_app.add_handler(CommandHandler("start", help_command))
    tg_app.add_handler(CommandHandler("help", help_command))
    tg_app.add_handler(CommandHandler("removemovie", remove_movie))
    tg_app.add_handler(CommandHandler("listmovies", list_movies))
    tg_app.add_handler(MessageHandler(filters.Document.ALL, file_info))
    
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

    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_movie_request))
    tg_app.add_handler(CallbackQueryHandler(send_movie))
    tg_app.add_handler(MessageHandler(filters.ALL, delete_message_later))

    print("Bot is running...")
    tg_app.run_polling()

if __name__ == "__main__":
    main()
