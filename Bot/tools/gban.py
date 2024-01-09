from pyrogram import filters, enums
from pyrogram.handlers import MessageHandler

from Bot import user, logger

async def gban(_, message):
    n

user.add_handler(MessageHandler(gban, filters=(filters.me & filters.command(['gban'], ['/','.',',','!']))))
