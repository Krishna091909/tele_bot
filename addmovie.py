from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from loadmovies import load_movies, save_movies

# Conversation States
MOVIE_NAME, FILE_ID, FILE_SIZE, FILE_NAME = range(4)
OWNER_ID = 7743703095  # Your Telegram ID

async def start_add_movie(update: Update, context: CallbackContext):
    """Start movie addition."""
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized.")
        return ConversationHandler.END
    await update.message.reply_text("🎬 Enter **Movie Name**:")
    return MOVIE_NAME

async def movie_name_handler(update: Update, context: CallbackContext):
    """Get movie name."""
    context.user_data["movie_name"] = update.message.text
    await update.message.reply_text("📂 Enter **File ID**:")
    return FILE_ID

async def file_id_handler(update: Update, context: CallbackContext):
    """Get file ID."""
    context.user_data["file_id"] = update.message.text
    await update.message.reply_text("📏 Enter **File Size** (e.g., 500MB):")
    return FILE_SIZE

async def file_size_handler(update: Update, context: CallbackContext):
    """Get file size."""
    context.user_data["file_size"] = update.message.text
    await update.message.reply_text("📄 Enter **File Name** (e.g., movie.mp4):")
    return FILE_NAME

async def file_name_handler(update: Update, context: CallbackContext):
    """Save movie details."""
    context.user_data["file_name"] = update.message.text

    # Store in Google Sheets
    movies = load_movies()
    movies[context.user_data["movie_name"]] = {
        "file_id": context.user_data["file_id"],
        "file_size": context.user_data["file_size"],
        "file_name": context.user_data["file_name"]
    }
    save_movies(movies)

    await update.message.reply_text(f"✅ **'{context.user_data['movie_name']}'** added successfully!")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    """Cancel process."""
    await update.message.reply_text("❌ Movie addition cancelled.")
    return ConversationHandler.END
