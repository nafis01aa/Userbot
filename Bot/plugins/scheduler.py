from random import randint
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot.utils.commands import UCommand
from Bot.functions.fstools import get_time
from Bot import user, user_scheduler, logger
from Bot.functions.asynctools import new_task

sorted_tasks = {}

async def scheduler_task():
    pass

@new_task
async def _schedule(_, message):
    if not message.reply_to_message:
        await message.edit('`Reply to a message`')
        return

    seconds = ''
    minutes = ''
    hours = ''
    mode = ''
    
    if len(message.command) > 1:
        try:
            mode = 'hours'
            seconds = int(message.command[1]) * 3600
        except ValueError:
            if 's' in message.command[1]:
                mode = 'seconds'
                seconds = int(message.command[1].replace('s', ''))
            elif 'm' in message.command[1]:
                mode = 'minutes'
                minutes = int(message.command[1].replace('m', ''))
            elif 'h' in message.command[1]:
                mode = 'hours'
                hours = int(message.command[1].replace('h', ''))
        except Exception as e:
            await message.edit(f'`{e}`')
            return
    else:
        mode = 'hours'
        hours = 1

    msg = message.reply_to_message
    task_id = user_scheduler.add_job(scheduler_task, 'interval', (msg),
                           seconds=seconds if seconds else 0,
                           minutes=minutes if minutes else 0,
                           hours=hours)

    content = msg.caption if msg.caption else msg.text
    sorted_tasks[task_id] = content[:10]
    await message.edit(f'`Post scheduled for every {} `')

user.add_handler(MessageHandler())
