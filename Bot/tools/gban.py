from time import sleep
from pyrogram import filters, enums
from pyrogram.handlers import MessageHandler

from Bot import user, logger

async def gban(_, message):
    chats = 0
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        if len(message.command) > 1:
            reason = message.text.split(maxsplit=1)[1]
        else:
            reason = None
    else:
        if len(message.command) < 2:
            await message.edit("`Reply to a user or provide user id`")
            sleep(1)
            await message.delete()
            return
        
        user_id = message.command[1]
        
        if len(message.command) > 2:
            reason = message.command[2]
        else:
            reason = None
    
    loading = await message.edit("`Gbanning...`")
    
    async for dialog in app.get_dialogs():
        if 
        js


user.add_handler(MessageHandler(gban, filters=(filters.me & filters.command(['gban'], ['/','.',',','!']))))
