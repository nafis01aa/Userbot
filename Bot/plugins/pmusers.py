from random import choice
from time import time, sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger, pm_hours
from Bot.utils.commands import UCommand
from Bot.functions.asynctools import new_task
from Bot.resources.imgs import pm_warn_imgs

counted = {}
previous_msg = {}

@new_task
async def on_pm(client, message):
    user_id = message.chat.id
    pm_hold = pm_hours * 3600

    if user_id in previous_msg:
        try:
            await user.delete_messages(message.chat.id, previous_msg[user_id])
        except:
            pass
    
    if user_id in counted:
        elapsed_time = time() - counted[user_id]
        
        if elapsed_time < int(pm_hold):
            return

    warn_photo = choice(pm_warn_imgs)
    warn_message = await message.reply_photo(photo=warn_photo, quote=True, caption="Please don't spam, I will come back soon!")
    previous_msg[user_id] = warn_message.id

@new_task
async def pmstop(client, message):
    _hold = pm_hours
    stop_warn = await message.edit(f"`Successfully stopped warning message for this chat for {_hold} hours`")
    user_id = message.chat.id
    counted[user_id] = time()
    sleep(1)

    if user_id in previous_msg:
        try:
            await user.delete_messages(message.chat.id, previous_msg[user_id])
        except:
            pass

    try:
        await user.delete_messages(message.chat.id, stop_warn.id)
    except:
        pass

user.add_handler(MessageHandler(on_pm, filters=(filters.private & ~filters.me)))
user.add_handler(MessageHandler(pmstop, filters=(filters.private & filters.me & filters.command(*UCommand.pmstop))))
