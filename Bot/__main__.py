from pyrogram import filters
from datetime import datetime
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
    startmsg = datetime.now()
    loading = await message.edit('Pinging...')
    endmsg = datetime.now()
    pings = (startmsg - endmsg).microseconds / 1000
    await message.edit(f'Ping - {pings} ms')

async def main():
    user.add_handler(MessageHandler(start, filters=filters.command('yo')))
    
    if bot:
        logger.info('Bot started! 🔥')
        bot.add_handler(MessageHandler(botstart, filters=filters.command('start')))

    logger.info('Userbot started! 🔥')

if bot:
    bot.loop.run_until_complete(main())
    bot.loop.run_forever()
else:
    user.loop.run_until_complete(main())
    user.loop.run_forever()
