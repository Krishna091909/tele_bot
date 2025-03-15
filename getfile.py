from telegram import Update
from telegram.ext import CallbackContext

async def file_info(update: Update, context: CallbackContext):
    document = update.message.document
    if document:
        file_size_bytes = document.file_size
        file_size_mb = file_size_bytes / (1024 * 1024)  
        file_name = document.file_name if document.file_name else "Unknown"
        file_id = document.file_id
        
        response = f"{file_name} {file_id} {file_size_mb:.2f}MB {file_name}"
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("❌ Please send a document file.")
