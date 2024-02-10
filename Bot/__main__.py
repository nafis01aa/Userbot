import sys
from time import time, sleep
from pyrogram import filters
from datetime import datetime
from signal import signal, SIGINT
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from Bot.functions.fstools import exiting
from Bot.utils.commands import BCommand, UCommand
from Bot.admintools import ban, gban, mute, purge
from Bot.plugins import alive, id, pmusers, restrictforwarder, scheduler
from Bot import user, user_scheduler, bot, bot_scheduler, starting_time, logger

async def yo(_, message):
    await message.edit('`Yoo!`')

async def botstart(_, message):
    await message.reply('**Welcome To Userbot!**')

async def ping(_, message):
    start_time = int(round(time() * 1000))
    loading = await message.edit('`wait..`')
    end_time = int(round(time() * 1000))
    await message.edit(f'`{end_time - start_time}` ms')

async def logs(_, message):
    with open('logs.txt', 'r') as log:
        logtextlines = log.read().splitlines()
    
    ind = 1
    Loglines = ''
    try:
        while len(Loglines) <= 1500:
            Loglines = f'{logtextlines[-ind]}\n{Loglines}'
            if ind == len(logtextlines):
                break

            ind += 1
        log_text = Loglines
        await message.edit(text=log_text, disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"{e}")

async def main():
    user.add_handler(MessageHandler(logs, filters=(filters.me & filters.command(*UCommand.log))))
    user.add_handler(MessageHandler(ping, filters=(filters.me & filters.command(*UCommand.ping))))
    user.add_handler(MessageHandler(yo, filters=(filters.me & filters.command(*UCommand.yo))))
    logger.info('Userbot started! 🔥')
    signal(SIGINT, exiting)

async def bot_main():
    bot.add_handler(MessageHandler(botstart, filters=filters.command(*BCommand.start)))
    logger.info('Bot started! 🔥')

if bot:
    bot.loop.run_until_complete(bot_main())

user.loop.run_until_complete(main())
user.loop.run_forever()
