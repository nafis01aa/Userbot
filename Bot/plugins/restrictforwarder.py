import re
from pyrogram import filters
from pyrogram.enums import MessageMediaType 
from pyrogram.handlers import MessageHandler

from Bot import user, logger, DOWNLOAD_DIR

def handle_media_groups(message, chat_id: int, message_id: int):
    InputList = []
    medias = user.get_media_group(chat_id=chat_id, message_id=message_id)

    for content in medias:
        path = user.download_media(message=content, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
        
        if content.media == MessageMediaType.VIDEO:
            InputList.append(InputMediaVideo(path, caption=content.caption))
        elif content.media == MessageMediaType.PHOTO:
            InputList.append(InputMediaPhoto(path, caption=content.caption))
        elif content.media == MessageMediaType.AUDIO:
            InputList.append(InputMediaAudio(path, caption=content.caption))
        elif content.media == MessageMediaType.DOCUMENT:
            InputList.append(InputMediaDocument(path, caption=content.caption))

    return InputList

def handle_forward(message, chat_id: int, message_id: int):
    try:
        msg = user.get_messages(chat_id=chat_id, message_ids=message_id)
    except Exception as e:
        logger.error(e)
        return {"status": False, "message": e}

    if msg.media and msg.media_group_id:
        medias = await sync_to_async(handle_media_groups, message, chat_id, message_id)
    elif msg.media and not msg.media_group_id:
        path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')

        message.edit("`Uploading..`")
        if msg.media == MessageMediaType.PHOTO:
            user.send_photo(message.chat.id, photo=path, caption=msg.caption, caption_entities=msg.entities)
        elif msg.media == MessageMediaType.VIDEO:
            user.send_video(message.chat.id, video=path, caption=msg.caption, caption_entities=msg.entities)
        elif msg.media == MessageMediaType.AUDIO:
            user.send_audio(message.chat.id, audio=path, caption=msg.caption, caption_entities=msg.entities)
        elif msg.media == MessageMediaType.DOCUMENT:
            user.send_document(message.chat.id, document=path, caption=msg.caption, caption_entities=msg.entities)
        elif msg.media == MessageMediaType.STICKER:
            user.send_sticker(message.chat.id, sticker=path)
        elif msg.media == MessageMediaType.ANIMATION:
            user.send_animation(message.chat.id, animation=path, caption=msg.caption, caption_entities=msg.entities)
        elif msg.media == MessageMediaType.VOICE:
            user.send_voice(message.chat.id, voice=path, caption=msg.caption, caption_entities=msg.entities)
        elif msg.media == MessageMediaType.VIDEO_NOTE:
            user.send_video_note(message.chat.id, video_note=path)
    else:
        user.send_message(message.chat.id, text=msg.text, entities=msg.entities)

async def on_forward(_, message):
    if len(message.command) < 2:
        await message.edit("`Provide me a message link`")
        return

    url = message.text.split(maxsplit=1)[1]
    match = re.search(r'https?://t\.me/[a-zA-Z0-9_]+', url)

    if match:
        url = match.group()
    else:
        await message.edit("`No Telegram Link Found!`")
        return
    
    message_id = url.split('/')[-1]

    if '?' in message_id:
        message_id = int(message_id.split('?', maxsplit=1)[0])
    else:
        message_id = int(message_id)
    
    if "t.me/c/" in url:
        chat_id = int('-100' + url.split('/')[-2])
    elif "t.me/b/" in url:
        chat_id = int(url.split('/')[-2])
    else:
        if "t.me/+" or "t.me/joinchat" in url:
            await message.edit("`Provide me a message link, not join/invite link`")
            return
        
        chat_id = url.split('/')[-2]

    await message.edit("`Downloading..`")
    

user.add_handler(MessageHandler(on_forward, filters=(filters.me & filters.command(['forward','getmsg'], ['/','.',',','!']))))
