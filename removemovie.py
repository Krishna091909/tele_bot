from telegram import Update
from telegram.ext import CallbackContext
from loadmovies import remove_movie

OWNER_ID = 7743703095  

async def remove_movie_command(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    movie_name = " ".join(context.args)
    if remove_movie(movie_name):
        await update.message.reply_text(f"🗑️ Movie '{movie_name}' removed successfully!")
    else:
        await update.message.reply_text("❌ Movie not found!")
