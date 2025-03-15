import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from loadmovies import load_movies
from deletemessages import delete_message_later

async def handle_movie_request(update: Update, context: CallbackContext):
    movies = load_movies()
    movie_name = update.message.text.lower()
    matched_movies = [key for key in movies.keys() if movie_name in key.lower()]

    if matched_movies:
        keyboard = [
            [InlineKeyboardButton(f"{movies[name]['file_size']} | {movies[name]['file_name']}", callback_data=name)]
            for name in matched_movies
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = await update.message.reply_text("🎬 Here is what I found for your query 👇:", reply_markup=reply_markup)
    else:
        msg = await update.message.reply_text("❌ Movie not found! Please check the spelling.")
    
    if update.message.chat.type in ["group", "supergroup"]:
        asyncio.create_task(delete_message_later(msg))
