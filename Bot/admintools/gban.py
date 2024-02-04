import asyncio
from time import sleep
from pyrogram import filters, enums
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler

from Bot import user, logger
from Bot.funcs.asynctools import new_task

@new_task
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
    await message.edit("`Gbanning...`")
    
    threshold_30 = False
    threshold_55 = False
    threshold_89 = False
    
    completion = 0
    total_dialogs = await user.get_dialogs_count()
    
    async for dialog in user.get_dialogs():
        if dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
            try:
                chat_id = dialog.chat.id
                await user.ban_chat_member(chat_id=chat_id, user_id=user_id)
                banned_chats += 1
            except FloodWait as e:
                logger.warning(f'Flood wait {e.value} seconds from GBanning!')
                await asyncio.sleep(e.value)
                chat_id = dialog.chat.id
                await user.ban_chat_member(chat_id=chat_id, user_id=user_id)
                banned_chats += 1
            except:
                pass
            
        completion += 1
        ban_percentage = (completion / total_dialogs) * 100
        
        if ban_percentage >= 30 and not threshold_30:
            threshold_30 = True
            await message.edit(f"**#Gbanning** `{get_user.first_name}... (30% completed)`")

        if ban_percentage >= 55 and not threshold_55:
            threshold_55 = True
            await message.edit(f"**#Gbanning** `{get_user.first_name}... (55% completed)`")

        if ban_percentage >= 89 and not threshold_89:
            threshold_89 = True
            await message.edit(f"**#Gbanning** `{get_user.first_name}... (89% completed)`")
    
    await message.edit(f"**#Gbanned** `{get_user.first_name} in {banned_chats} chats and removed!`")

user.add_handler(MessageHandler(gban, filters=(filters.me & filters.command(['gban'], ['/','.',',','!']))))
