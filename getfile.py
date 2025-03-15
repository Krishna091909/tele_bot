from telegram import Update
from telegram.ext import CallbackContext

async def file_info(update: Update, context: CallbackContext):
    document = update.message.document
    if document:
        file_size_bytes = document.file_size
        file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to MB
        file_name = document.file_name if document.file_name else "Unknown"
        file_id = document.file_id
        
        response = f"📁 *File Name:* `{file_name}`\n📦 *Size:* `{file_size_mb:.2f}MB`\n🆔 *File ID:* `{file_id}`"
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Please send a document file.")
