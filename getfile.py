from telegram import Update
from telegram.ext import CallbackContext

# Get file ID, Size & Name (Owner Only)
async def get_file_id(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    document = update.message.document
    if document:
        file_size_bytes = document.file_size
        file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to MB

        await update.message.reply_text(
            f"`{document.file_id}` `{file_size_mb:.2f}MB` `{document.file_name}`",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("⚠️ Please send a movie file to get its ID.")

