from time import sleep
from pyrogram import filters, enums
from pyrogram.types import ChatPermissions
from pyrogram.handlers import MessageHandler

from Bot import user, logger

async def mute(_, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.edit("`This plugin works in groups or supergroups only!`")
        return

    get_me = await user.get_chat_member(chat_id=message.chat.id, "me")
    if get_me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.edit("`I am not admin, lul!`")
        sleep(1)
        await message.delete()
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        if (message.command) < 2:
            await message.edit('`Reply to a user or provide user id`')
            return

        user_id = message.command[1]

    try:
        await user.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, ChatPermissions())
        user_link = f"[User](tg://user?id={user_id})"
        await message.edit(f"{user_link} `is muted!`")
    except Exception as e:
        await message.edit(f"`ERROR: {e}`")

async def unmute(_, message):
    if message.chat.type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        await message.edit("`This plugin works in groups or supergroups only!`")
        return

    get_me = await user.get_chat_member(chat_id=message.chat.id, "me")
    if get_me.status not in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.edit("`I am not admin, lul!`")
        sleep(1)
        await message.delete()
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        if (message.command) < 2:
            await message.edit('`Reply to a user or provide user id`')
            return

        user_id = message.command[1]

    try:
        await user.restrict_chat_member(chat_id=message.chat.id, user_id=user_id, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True))
        user_link = f"[User](tg://user?id={user_id})"
        await message.edit(f"{user_link} `is unmuted! ✅`")
    except Exception as e:
        await message.edit(f"`ERROR: {e}`")

user.add_handler(MessageHandler(mute, filters=(filters.me & filters.command(['mute'], ['/','.',',','!']))))
user.add_handler(MessageHandler(unmute, filters=(filters.me & filters.command(['unmute'], ['/','.',',','!']))))
