import sys
from time import time, sleep
from pyrogram import filters
from datetime import datetime
from signal import signal, SIGINT
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from Bot.funcs.fstools import exiting
from Bot.admintools import ban, gban, mute, purge
from Bot.plugins import alive, id, pmusers, restrictforwarder
from Bot import user, user_scheduler, bot, bot_scheduler, starting_time, logger

async def yo(_, message):
    text = (
        f'**Yoo!**'
    )
    await message.edit(text)

async def botstart(_, message):
    text = (
        f'**Welcome To Userbot!**'
    )
    await message.reply(text)

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
        while len(Loglines) <= 2500:
            Loglines = f'{logtextlines[-ind]}\n{Loglines}'
            
            if ind == len(logtextlines):
                break
            
            ind += 1
        
        log_text = Loglines
        await message.edit(text=log_text, disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"{e}")

async def main():
    user.add_handler(MessageHandler(yo, filters=(filters.me & filters.command(['yo'], ['/','.',',','!']))))
    user.add_handler(MessageHandler(logs, filters=(filters.me & filters.command(['log','logs'], ['/','.',',','!']))))
    user.add_handler(MessageHandler(ping, filters=(filters.me & filters.command(['ping'], ['/','.',',','!']))))
    
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
