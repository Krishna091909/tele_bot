from telegram import Update
from telegram.ext import CallbackContext

async def file_info(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    document = update.message.document
    if document:
        await update.message.reply_text(f"File ID: `{document.file_id}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("Please send a movie file.")
