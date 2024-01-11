from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot import user, logger

def get_ids(from_id: int, to_id: int):
    current_id = from_id

    while current_id < to_id:
        yield list(range(current_id, min(current_id + 100, to_id)))
        current_id += 100

async def purge(_, message):
    if message.reply_to_message:
        from_msg_id = message.reply_to_message.id
    else:
        if len(message.command) < 2:
            await message.edit("`Reply to a message or give me a message id to start purge from that to all!`")
            return

        from_msg_id = int(message.command[1])
    
    await message.edit("`Purging...`")
    
    for msg_ids in get_ids(from_msg_id, message.id + 1):
        try:

user.add_handler()
