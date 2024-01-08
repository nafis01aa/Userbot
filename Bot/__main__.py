import sys
from time import time, sleep
from pyrogram import filters
from datetime import datetime
from signal import signal, SIGINT
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from Bot import user, bot, starting_time, logger

async def yo(client, message):
    text = (
        f'**Yoo!**'
    )
    await message.edit(text)

async def botstart(client, message):
    text = (
        f'**Welcome To Userbot!**'
    )
    await message.reply(text)

async def ping(client, message):
    start_time = int(round(time() * 1000))
    loading = await message.edit('`wait..`')
    end_time = int(round(time() * 1000))
    await message.edit(f'`{end_time - start_time}` ms')

def exiting(signal, frame):
    if bot:
        
    logger.info('Exiting deploy..!')
    sys.exit(0)

async def main():
    user.add_handler(MessageHandler(yo, filters=filters.command('yo')))
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
