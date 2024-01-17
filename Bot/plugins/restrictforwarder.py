from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger

async def on_forward(_, message):
    if len(message.command) < 2:
        await message.edit("`Provide me a message link`")
        return

    url = message.command[1]
    message_id = int(url.split('/')[-1])
    
    if "t.me/c/" in url:
        chat_id = int('-100' + url.split('/')[-2])
    else:
        chat_id = url.split('/')[-2]

user.add_handler(MessageHandler(on_forward, filters=(filters.me & filters.command(['forward','getmsg'], ['/','.',',','!']))))
