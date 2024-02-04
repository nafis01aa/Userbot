from random import choice
from time import time, sleep
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot.utils.commands import 
from Bot.functions.fstools import get_time
from Bot.resources.imgs import alive_imgs
from Bot.functions.asynctools import new_task
from Bot import user, logger, starting_time, user_full_name, user_userid

@new_task
async def _alive(_, message):
    start_time = int(round(time() * 1000))
    await message.edit('`..`')
    end_time = int(round(time() * 1000))
    uptime = get_time(time() - starting_time)
    alive_image = choice(alive_imgs)
    owner_link = f"[{user_full_name}](tg://user?id={user_userid})"
    alive_msg = (
        f'**--I AM ALIVE--**\n\n'
        f'**◍ UPTIME:-** {uptime}\n'
        f'**◍ STATUS:-** Cool 🔥\n'
        f'**◍ PING:-** {end_time - start_time} ms\n'
        f'**◍ OWNER:-** {owner_link}'
    )
    await message.delete()
    await user.send_photo(chat_id=message.chat.id, photo=alive_image, caption=alive_msg)

user.add_handler(MessageHandler(_alive, filters=(filters.me & filters.command(['alive'], ['/','.',',','!']))))
