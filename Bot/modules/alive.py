from time import time, sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger
from Bot.funcs.fstools import get_time

async def alive(_, message):
    right_now = time() - 
    uptime = get_time()
    await message.edit('`..`')
    alive_msg = (
        f'**--I Am Alive--**\n\n'
        f'**UPTIME:- {}'
    )
