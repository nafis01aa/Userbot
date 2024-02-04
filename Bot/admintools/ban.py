from time import sleep
from pyrogram import filters, enums
from datetime import datetime, timedelta
from pyrogram.types import ChatPermissions
from pyrogram.handlers import MessageHandler

from Bot import user, logger
from Bot.utils.commands import UCommand
from Bot.funcs.asynctools import new_task

@new_task
async def ban(_, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.edit("`This plugin works in groups and supergroups only!`")
        sleep(1)
        await message.delete()
        return

    get_me = await user.get_chat_member(chat_id=message.chat.id, user_id="me")
    if get_me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.edit("`I am not admin, lul!`")
        sleep(1)
        await message.delete()
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        
        if len(message.command) > 1:
            duration = message.command[1]
        else:
            duration = None
    else:
        if len(message.command) < 2:
            await message.edit('`Reply to a user or provide user id`')
            sleep(1)
            await message.delete()
            return

        user_id = message.command[1]
        
        if len(message.command) > 2:
            duration = message.command[2]
        else:
            duration = None

    try:
        if duration:
            await user.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=(datetime.now() + timedelta(hours=int(duration))))
        else:
            await user.ban_chat_member(chat_id=message.chat.id, user_id=user_id)
        
        user_link = f"[User](tg://user?id={user_id})"
        if duration:
            await message.edit(f"{user_link} `is banned for {duration} hours! 🚫`")
        else:
            await message.edit(f"{user_link} `is banned forever! ❌`")
        sleep(3)
        await message.delete()
    except Exception as e:
        await message.edit(f"`ERROR: {e}`")

@new_task
async def unban(_, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.edit("`This plugin works in groups and supergroups only!`")
        sleep(1)
        await message.delete()
        return

    get_me = await user.get_chat_member(chat_id=message.chat.id, user_id="me")
    if get_me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.edit("`I am not admin, lul!`")
        sleep(1)
        await message.delete()
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        if len(message.command) < 2:
            await message.edit('`Reply to a user or provide user id`')
            sleep(1)
            await message.delete()
            return

        user_id = message.command[1]

    try:
        await user.unban_chat_member(chat_id=message.chat.id, user_id=user_id)
        user_link = f"[User](tg://user?id={user_id})"
        await message.edit(f"{user_link} `is unbanned in this chat! 💕`")
        sleep(3)
        await message.delete()
    except Exception as e:
        await message.edit(f"`ERROR: {e}`")

user.add_handler(MessageHandler(ban, filters=(filters.me & filters.command(*UCommand.ban))))
user.add_handler(MessageHandler(unban, filters=(filters.me & filters.command(*UCommand.unban))))
