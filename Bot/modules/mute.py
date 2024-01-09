from pyrogram import filters, enums
from pyrogram.handlers import MessageHandler

from Bot import user, logger

async def mute(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        if (message.command) < 2:
            await message.edit('`Reply to a user or provide user id`')
            return

        user_id = message.command[1]

    b
