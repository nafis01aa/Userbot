import re
from pyrogram import filters
from pyrogram.enums import MessageMediaType 
from pyrogram.handlers import MessageHandler
from pyrogram.errors import ChatForwardsRestricted
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument

from Bot import user, logger, DOWNLOAD_DIR
from Bot.funcs.fstools import clean_download
from Bot.funcs.asynctools import new_task, sync_to_async

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

    message.edit("`Uploading..`")
    user.send_media_group(message.chat.id, media=InputList)
    message.delete()

def handle_forward(message, msg):
    if msg.media:
        message.edit("`Uploading..`")
        if msg.media == MessageMediaType.PHOTO:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_photo(message.chat.id, photo=path, caption=msg.caption, caption_entities=msg.entities)
            message.delete()
        elif msg.media == MessageMediaType.VIDEO:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_video(message.chat.id, video=path, caption=msg.caption, caption_entities=msg.entities)
            message.delete()
        elif msg.media == MessageMediaType.AUDIO:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_audio(message.chat.id, audio=path, caption=msg.caption, caption_entities=msg.entities)
            message.delete()
        elif msg.media == MessageMediaType.DOCUMENT:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_document(message.chat.id, document=path, caption=msg.caption, caption_entities=msg.entities)
            message.delete()
        elif msg.media == MessageMediaType.STICKER:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_sticker(message.chat.id, sticker=path)
            message.delete()
        elif msg.media == MessageMediaType.ANIMATION:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_animation(message.chat.id, animation=path, caption=msg.caption, caption_entities=msg.entities)
            message.delete()
        elif msg.media == MessageMediaType.VOICE:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_voice(message.chat.id, voice=path, caption=msg.caption, caption_entities=msg.entities)
            message.delete()
        elif msg.media == MessageMediaType.VIDEO_NOTE:
            path = user.download_media(message=msg, file_name=f'{DOWNLOAD_DIR}/{message.id}/')
            user.send_video_note(message.chat.id, video_note=path)
            message.delete()
        elif msg.media == MessageMediaType.WEB_PAGE:
            message.delete()
            user.send_message(message.chat.id, text=msg.text, entities=msg.entities)
    else:
        message.delete()
        user.send_message(message.chat.id, text=msg.text, entities=msg.entities)

@new_task
async def on_forward(_, message):
    if len(message.command) < 2:
        await message.edit("`Provide me a message link`")
        return

    url = message.text.split(maxsplit=1)[1]
    match = re.search(r'https?://t\.me/[^\s<>"]+', url)

    if match:
        url = match.group()
    else:
        await message.edit("`No Telegram Link Found!`")
        return
    
    if "https://t.me/+" in url or "https://t.me/joinchat/" in url:
        await message.edit("`Provide me a message link, not join/invite link`")
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
        chat_id = url.split('/')[-2]

    await message.edit("`Downloading..`")
    
    try:
        msg = await user.get_messages(chat_id=chat_id, message_ids=message_id)
    except Exception as e:
        logger.error(e)
        await message.edit(f"Error: {e}")
        return

    if msg.media and msg.media_group_id:
        try:
            await msg.copy(chat_id=message.chat.id)
            await message.delete()
        except ChatForwardsRestricted:
            await sync_to_async(handle_media_groups, message, chat_id, message_id)
    else:
        try:
            await msg.copy(chat_id=message.chat.id)
            await message.delete()
        except ChatForwardsRestricted:
            await sync_to_async(handle_forward, message, msg)

    await clean_download(f'{DOWNLOAD_DIR}/{message.id}')

user.add_handler(MessageHandler(on_forward, filters=(filters.me & filters.command(['forward','getmsg'], ['/','.',',','!']))))
