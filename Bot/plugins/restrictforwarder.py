from pyrogram import filters
from pyrogram.enums import MessageMediaType 
from pyrogram.handlers import MessageHandler

from Bot import user, logger

def handle_media_groups(chat_id: int, message_id: int):
    InputList = []
    medias = await user.get_media_group(chat_id=chat_id, message_id=message_id)

    for content in medias:
        if content.media == enums.MessageMediaType.VIDEO:

def handle_forward(message, chat_id: int, message_id: int):
    try:
        msg = user.get_messages(chat_id=chat_id, message_ids=message_id)
    except Exception as e:
        logger.error(e)
        return {"status": False, "message": e}

    if msg.media and msg.media_group_id

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
