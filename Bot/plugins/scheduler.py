from random import randint
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger
from Bot.utils.commands import UCommand
from Bot.functions.fstools import get_time
from Bot.functions.asynctools import new_task

@new_task
async def _schedule(_, message):
    if not message.reply_to_message:
        await message.edit('`Reply to a message`')
        return

    msg = message.reply_to_message
    task_id = f'{message.reply_to_message.id}{randint(100, 999)}'
    -

user.add_handler(MessageHandler())
