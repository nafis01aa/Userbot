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
    else:
        h

async def on_forward(_, message):
    if len(message.command) < 2:
        await message.edit("`Provide me a message link`")
        return

    url = message.command[1]
    message_id = url.split('/')[-1]

    if '?' in message_id:
        message_id = int(message_id.split('?', maxsplit=1)[0])
    else:
        message_id = int(message_id)
    
    if "t.me/c/" in url:
        chat_id = int('-100' + url.split('/')[-2])
    else:
        chat_id = url.split('/')[-2]

user.add_handler(MessageHandler(on_forward, filters=(filters.me & filters.command(['forward','getmsg'], ['/','.',',','!']))))
