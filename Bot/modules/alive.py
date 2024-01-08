from time import time, sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot.funcs.fstools import get_time
from Bot import user, logger, starting_time

async def alive(_, message):
    start_time = int(round(time() * 1000))
    await message.edit('`..`')
    end_time = int(round(time() * 1000))
    uptime = get_time(time() - starting_time)
    alive_msg = (
        f'**--I Am Online--**\n\n'
        f'**UPTIME:-** {uptime}\n'
        f'**STATUS:-** Cool 🔥\n'
        f'**PING:-** {end_time - start_time} ms'
    )
