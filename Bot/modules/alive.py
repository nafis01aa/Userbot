from time import time, sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger, pm_hours

async def alive(_, message):
    uptime = 
    await message.edit('`..`')
    alive_msg = (
        f'**--I Am Alive--**\n\n'
        f'**UPTIME:- {}'
    )
