from pyrogram import Client
from typing import Any, Optional
from pyrogram.types import Message
from pyrogram.file_id import FileId
from pyrogram.raw.types.messages import Messages
from Jisshu.server.exceptions import FIleNotFound


async def parse_file_id(message: "Message") -> Optional[FileId]:
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

async def parse_file_unique_id(message: "Messages") -> Optional[str]:
    media = get_media_from_message(message)
    if media:
        return media.file_unique_id

async def get_file_ids(client: Client, chat_id: int, id: int) -> Optional[FileId]:
    message = await client.get_messages(chat_id, id)
    if message.empty:
        raise FIleNotFound
    media = get_media_from_message(message)
    file_unique_id = await parse_file_unique_id(message)
    file_id = await parse_file_id(message)
    setattr(file_id, "file_size", getattr(media, "file_size", 0))
    setattr(file_id, "mime_type", getattr(media, "mime_type", ""))
    setattr(file_id, "file_name", getattr(media, "file_name", ""))
    setattr(file_id, "unique_id", file_unique_id)
    return file_id

def get_media_from_message(message: "Message") -> Any:
    """
    Extracts media from a given message.

    Args:
        message (Message): The message object from which to extract media.

    Returns:
        Any: The media object if found; otherwise, None.
    """
    media_types = [
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    ]

    for media_type in media_types:
        media = getattr(message, media_type, None)
        if media:
            return media
            
    return None  # Explicitly return None if no media found

def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]

def get_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, 'file_name', "")

def get_media_file_size(m):
    media = get_media_from_message(m)
    return getattr(media, "file_size", 0)
