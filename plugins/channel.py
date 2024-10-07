# Credit - JISSHU BOTS
# Modified By NBBotz
# Some Codes Are Taken From A GitHub Repository And We Forgot His Name
# Base Code Bishal

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import CHANNELS, MOVIE_UPDATE_CHANNEL, ADMINS , LOG_CHANNEL
from database.ia_filterdb import save_file, unpack_new_file_id
from utils import get_poster, temp
import re
from database.users_chats_db import db

processed_movies = set()
media_filter = filters.document | filters.video

media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    bot_id = bot.me.id
    media = getattr(message, message.media.value, None)
    if media.mime_type in ['video/mp4', 'video/x-matroska']: 
        media.file_type = message.media.value
        media.caption = message.caption
        success_sts = await save_file(media)
        if success_sts == 'suc' and await db.get_send_movie_update_status(bot_id):
            file_id, file_ref = unpack_new_file_id(media.file_id)
            await send_movie_updates(bot, file_name=media.file_name, caption=media.caption, file_id=file_id)

async def get_imdb(file_name):
    imdb_file_name = await movie_name_format(file_name)
    imdb = await get_poster(imdb_file_name)
    if imdb:
        return imdb.get('poster')
    return None
    
async def movie_name_format(file_name):
  filename = re.sub(r'http\S+', '', re.sub(r'@\w+|#\w+', '', file_name).replace('_', ' ').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('{', '').replace('}', '').replace('.', ' ').replace('@', '').replace(':', '').replace(';', '').replace("'", '').replace('-', '').replace('!', '')).strip()
  return filename

async def check_qualities(text, qualities: list):
    quality = []
    for q in qualities:
        if q in text:
            quality.append(q)
    quality = ", ".join(quality)
    return quality[:-2] if quality.endswith(", ") else quality

async def send_movie_updates(bot, file_name, caption, file_id, message):
    try:
        # Your existing logic to extract year, season, quality, etc.

        # Format movie name
        movie_name = await movie_name_format(file_name)
        if movie_name in processed_movies:
            return
        processed_movies.add(movie_name)

        # Try to get the IMDb poster first
        poster_url = await get_imdb(movie_name)

        # If IMDb poster is not available, fall back to the file's thumbnail
        if not poster_url:
            if message.document and message.document.thumb:
                # Use the document's thumbnail
                poster_url = message.document.thumb.file_id
                print("Using document thumbnail.")
            elif message.video and message.video.thumb:
                # Use the video's thumbnail
                poster_url = message.video.thumb.file_id
                print("Using video thumbnail.")
            else:
                # No IMDb poster or file thumbnail, use a fallback image
                poster_url = "https://telegra.ph/file/88d845b4f8a024a71465d.jpg"
                print("Using fallback poster.")

        # Caption for the update
        caption_message = f"#New_File_Added ✅\n\nFile_Name:- <code>{movie_name}</code>\n\nLanguage:- {language}\n\nQuality:- {quality}"

        # Buttons for the update
        movie_update_channel = await db.movies_update_channel_id()
        btn = [
            [InlineKeyboardButton('Get File', url=f'https://t.me/{temp.U_NAME}?start=pm_mode_file_{ADMINS[0]}_{file_id}')]
        ]
        reply_markup = InlineKeyboardMarkup(btn)

        # Send the poster (either IMDb, thumbnail, or fallback)
        await bot.send_photo(
            movie_update_channel if movie_update_channel else MOVIE_UPDATE_CHANNEL,
            photo=poster_url,
            caption=caption_message,
            reply_markup=reply_markup
        )

    except Exception as e:
        print('Failed to send movie update. Error - ', e)
        await bot.send_message(LOG_CHANNEL, f'Failed to send movie update. Error - {e}')
