from telegram import Update
from telegram.ext import CallbackContext
from loadmovies import load_movies, save_movies

OWNER_ID = 7743703095  

async def add_movie(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    args = context.args
    if len(args) < 4:
        await update.message.reply_text("⚠️ Usage: /addmovie <movie_name> <file_id> <file_size> <file_name>")
        return

    movie_name = " ".join(args[:-3])  
    file_id = args[-3]  
    file_size = args[-2]  
    file_name = args[-1]  

    movies = load_movies()
    movies[movie_name] = {
        "file_id": file_id,
        "file_size": file_size,
        "file_name": file_name
    }
    save_movies(movies)
    await update.message.reply_text(f"✅ Movie '{movie_name}' added successfully!")
