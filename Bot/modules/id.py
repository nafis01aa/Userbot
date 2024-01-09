from pyrogram import filters, enums
from pyrogram.handlers import MessageHandler

from Bot import user, logger

async def get_id(_, message):
    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
    else:
        replied_user = None

    replying_info = ''
    my_parmalink = f"[Here](tg://user?id={message.from_user.id})"

    if replied_user:
        replied_user_id = replied_user.id
        replied_user_name = replied_user.username
        replied_user_fn = replied_user.first_name if replied_user.first_name else 'Anonymous'
        replied_user_ln = replied_user.last_name if replied_user.last_name else ''
        replied_user_full_name = (f'{replied_user_fn} {replied_user_ln}').strip()
        replied_user_parmalink = f"[Here](tg://user?id={replied_user_id})"
        replying_info = (
            f'• **REPLIED USER INFO** •\n\n'
            f'• **ID:-** `{replied_user_id}`\n'
            f'• **USERNAME:-** @{replied_user_name}\n'
            f'• **FULL NAME:-** `{replied_user_full_name}`\n'
            f'• **PARMALINK:-** {replied_user_parmalink}'
        )

    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        id_msg = (
            f'• **MY ID:-** `{message.from_user.id}`\n'
            f'• **CHAT ID:-** `{message.chat.id}`\n'
            f'• **MY PARMALINK:-** {my_parmalink}\n\n'
            f'{replying_info}'
        )
    else:
        id_msg = (
            f'• **MY ID:-** `{message.from_user.id}`\n'
            f'• **MY PARMALINK:-** {my_parmalink}\n\n'
            f'{replying_info}'
        )
    await message.edit(id_msg, disable_web_page_preview=True)

user.add_handler(MessageHandler(get_id, filters=(filters.me & filters.command(['id'], ['/','.',',','!']))))
