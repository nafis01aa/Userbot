from time import sleep
from pyrogram import filters, enums
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

    user.restrict_chat_member(chat_id=message.chat.id, )
