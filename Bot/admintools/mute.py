from time import sleep
from pyrogram import filters, enums
from datetime import datetime, timedelta
from pyrogram.types import ChatPermissions
from pyrogram.handlers import MessageHandler

from Bot import user, logger
from Bot.utils.commands import UCommand
from Bot.functions.asynctools import new_task

@new_task
async def mute(_, message):
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
            await user.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=ChatPermissions(), until_date=(datetime.now() + timedelta(hours=int(duration))))
        else:
            await user.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=ChatPermissions())
        
        user_link = f"[User](tg://user?id={user_id})"
        if duration:
            await message.edit(f"{user_link} `is muted for {duration} hours! ⛔`")
        else:
            await message.edit(f"{user_link} `is muted forever! ⛔`")
        sleep(3)
        await message.delete()
    except Exception as e:
        await message.edit(f"`ERROR: {e}`")

@new_task
async def unmute(_, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.edit("`This plugin works in groups or supergroups only!`")
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
        await user.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, permissions=ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
        user_link = f"[User](tg://user?id={user_id})"
        await message.edit(f"{user_link} `is unmuted in this chat! ✅`")
        sleep(3)
        await message.delete()
    except Exception as e:
        await message.edit(f"`ERROR: {e}`")

user.add_handler(MessageHandler(mute, filters=(filters.me & filters.command(*UCommand.mute))))
user.add_handler(MessageHandler(unmute, filters=(filters.me & filters.command(*UCommand.unmute))))
