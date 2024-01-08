from pyrogram import filters
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

async def main():
    if bot:
        bot.add_handler(MessageHandler(botstart, filters=filters.command('start')))
    user.add_handler(MessageHandler(start, filters=filters.command('start')))

if bot:
    bot.loop.run_until_complete(main())
    bot.loop.run_forever()
else:
    user.loop.run_until_complete(main())
    user.loop.run_forever()
