from time import time, sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger, pm_hours

counted = {}

async def on_pm(client, message):
    user_id = message.chat.id
    pm_hold = pm_hours * 3600
    
    if user_id in counted:
        elapsed_time = time() - counted[user_id]
        
        if elapsed_time < int(pm_hold):
            return
    
    warn_message = await message.reply("Please don't spam, I will come back soon!")
    sleep(1)
    
    try:
        await user.delete_messages(message.chat.id, warn_message.id)
    except:
        pass

async def stop(client, message):
    _hold = pm_hours
    stop_warn = await message.edit(f"`Successfully stopped warning message for this chat for {_hold} hours`")
    user_id = message.chat.id
    counted[user_id] = time()
    sleep(0.5)
    
    try:
        await user.delete_messages(message.chat.id, stop_warn.id)
    except:
        pass

user.add_handler(MessageHandler(on_pm, filters=(filters.private & ~filters.me)))
user.add_handler(MessageHandler(stop, filters=(filters.private & filters.me & filters.command(['stop'], ['/','.',',']))))
