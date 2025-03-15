from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
from loadmovies import load_movies, save_movies

# Define conversation states
MOVIE_NAME, FILE_ID, FILE_SIZE, FILE_NAME = range(4)

OWNER_ID = 7743703095  # Your Telegram ID

async def start_add_movie(update: Update, context: CallbackContext):
    """Start the movie addition process by asking for the movie name."""
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return ConversationHandler.END

    await update.message.reply_text("🎬 Please enter the **Movie Name**:")
    return MOVIE_NAME

async def movie_name_handler(update: Update, context: CallbackContext):
    """Save movie name and ask for File ID."""
    context.user_data["movie_name"] = update.message.text
    await update.message.reply_text("📂 Now, please enter the **File ID**:")
    return FILE_ID

async def file_id_handler(update: Update, context: CallbackContext):
    """Save file ID and ask for File Size."""
    context.user_data["file_id"] = update.message.text
    await update.message.reply_text("📏 Now, please enter the **File Size** (e.g., 541.92MB):")
    return FILE_SIZE

async def file_size_handler(update: Update, context: CallbackContext):
    """Save file size and ask for File Name."""
    context.user_data["file_size"] = update.message.text
    await update.message.reply_text("📄 Finally, please enter the **File Name** (including extension, e.g., movie.mkv):")
    return FILE_NAME

async def file_name_handler(update: Update, context: CallbackContext):
    """Save file name, store details, and complete the process."""
    context.user_data["file_name"] = update.message.text

    # Store movie details
    movies = load_movies()
    movies[context.user_data["movie_name"]] = {
        "file_id": context.user_data["file_id"],
        "file_size": context.user_data["file_size"],
        "file_name": context.user_data["file_name"]
    }
    save_movies(movies)

    # Confirm movie addition
    await update.message.reply_text(
        f"✅ Movie **'{context.user_data['movie_name']}'** added successfully!\n"
        f"📂 **File ID:** `{context.user_data['file_id']}`\n"
        f"📏 **Size:** {context.user_data['file_size']}\n"
        f"📄 **File Name:** {context.user_data['file_name']}"
    )

    # End conversation
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    """Cancel the process if user changes their mind."""
    await update.message.reply_text("❌ Movie addition cancelled.")
    return ConversationHandler.END
