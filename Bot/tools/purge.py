from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger
from Bot.funcs.asynctools import new_task

def get_ids(from_id: int, to_id: int):
    current_id = from_id

    while current_id < to_id:
        yield list(range(current_id, min(current_id + 100, to_id)))
        current_id += 100

@new_task
async def purge(_, message):
    if message.reply_to_message:
        from_msg_id = message.reply_to_message.id
    else:
        if len(message.command) < 2:
            await message.edit("`Reply to a message or give me a message id to start purge from that to all!`")
            return

        from_msg_id = int(message.command[1])

    del_counts = 0
    await message.edit("`Purging in progress...`")
    
    for msg_ids in get_ids(from_msg_id, message.id + 1):
        try:
            last_deletes = await user.delete_messages(chat_id=message.chat.id, message_ids=msg_ids)
            del_counts += last_deletes
        except:
            pass

user.add_handler()
