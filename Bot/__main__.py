import sys
from time import sleep
from pyrogram import filters
from datetime import datetime
from signal import signal, SIGINT
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from Bot import user, bot, starting_time, logger

async def start(client, message):
    text = (
        f'**Welcome boss!**'
    )
    await message.edit(text)

async def botstart(client, message):
    text = (
        f'**Welcome To Userbot!**'
    )
    await message.reply(text)

async def ping(client, message):
    startmsg = int(round(time() * 1000))
    loading = await message.edit('`wait..`')
    endmsg = int(round(time() * 1000))
    pings = startmsg - endmsg
    await message.edit(f'`{pings}` ms')

async def exiting(signal, frame):
    logger.info('Exiting deploy..!')
    sys.exit(0)

async def main():
    user.add_handler(MessageHandler(start, filters=filters.command('yo')))
    user.add_handler(MessageHandler(ping, filters=filters.command('ping')))
    
    if bot:
        logger.info('Bot started! 🔥')
        sleep(1)
        bot.add_handler(MessageHandler(botstart, filters=filters.command('start')))

    logger.info('Userbot started! 🔥')
    signal(SIGINT, exiting)

if bot:
    bot.loop.run_until_complete(main())
    bot.loop.run_forever()
else:
    user.loop.run_until_complete(main())
    user.loop.run_forever()
