import asyncio
from telegram import Update
from telegram.ext import CallbackContext
from loadmovies import load_movies
from deletemessages import delete_message_later

async def send_movie(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    movie_name = query.data
    movies = load_movies()
    movie_data = movies.get(movie_name)

    if movie_data:
        user_id = query.from_user.id  
        file_id = movie_data["file_id"]
        file_size = movie_data["file_size"]
        file_name = movie_data["file_name"]

        await context.bot.send_document(
            chat_id=user_id, 
            document=file_id, 
            caption=f"🎬 *{file_name}*\n📦 *Size:* {file_size}",
            parse_mode="Markdown"
        )
        
        msg = await query.message.reply_text("📩 Check your DM for the movie file!")
        
        if query.message.chat.type in ["group", "supergroup"]:
            asyncio.create_task(delete_message_later(msg))
    else:
        await query.message.reply_text("❌ Movie not found.")
