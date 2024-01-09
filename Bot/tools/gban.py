import asyncio
from time import sleep
from pyrogram import filters, enums
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler

from Bot import user, logger

async def gban(_, message):
    banned_chats = 0
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

    get_user = await user.get_chat(user_id)
    loading = await message.edit("`Gbanning...`")
    
    async for dialog in app.get_dialogs():
        try:
            chat_id = dialog.chat.id
            await user.ban_chat_member(chat_id=chat_id, user_id=user_id)
            banned_chats += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            chat_id = dialog.chat.id
            await user.ban_chat_member(chat_id=chat_id, user_id=user_id)
            banned_chats += 1
        except:
            pass

    await message.edit("**#Gbanned** `{get_user.first_name} in {banned_chats} chats and removed!`")

user.add_handler(MessageHandler(gban, filters=(filters.me & filters.command(['gban'], ['/','.',',','!']))))
