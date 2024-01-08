from pyrogram import filters, enums
from pyrogram.handlers import MessageHandler

from Bot import user, logger, starting_time, user_full_name, user_userid

async def get_id(_, message):
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
    else:
        replied_user = None

    replied_user_id = ''
    replied_user_name = ''
    replied_user_full_name = ''

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        id_msg = (
            f''
