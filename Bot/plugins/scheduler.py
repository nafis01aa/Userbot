from random import randint
from pyrogram import filters
from pyrogram.handlers import MessageHandler

from Bot.utils.commands import UCommand
from Bot.functions.fstools import get_time
from Bot import user, user_scheduler, logger
from Bot.functions.asynctools import new_task

async def scheduler_task(chat_id, message):
    try:
        await message.copy(chat_id=chat_id)
    except:
        pass

@new_task
async def _schedule(_, message):
    if not message.reply_to_message:
        await message.edit('`Reply to a message`')
        return

    val = ''
    mode = ''
    
    if len(message.command) > 1:
        try:
            mode = 'hours'
            val = message.command[1]
            seconds = int(message.command[1]) * 3600
        except ValueError:
            if 's' in message.command[1]:
                mode = 'seconds'
                seconds = int(message.command[1].replace('s', ''))
                val = seconds
            elif 'm' in message.command[1]:
                mode = 'minutes'
                val = int(message.command[1].replace('m', ''))
                seconds = int(message.command[1].replace('m', '')) * 60
            elif 'h' in message.command[1]:
                mode = 'hours'
                val = int(message.command[1].replace('h', ''))
                seconds = int(message.command[1].replace('h', '')) * 3600
        except Exception as e:
            await message.edit(f'`{e}`')
            return
    else:
        val = 1
        mode = 'hours'
        seconds = 3600

    content = msg.caption if msg.caption else msg.text
    task_id = f'{message.chat.id}:{content[:10]}'
    msg = message.reply_to_message
    user_scheduler.add_job(scheduler_task,
                                     'interval',
                                     (chat_id, msg),
                                     seconds=seconds,
                                    id=task_id)

    await message.edit(f'`Post scheduled for every {val} {mode}`')

@new_task
async def _schedules(_, message):
    chat_id = message.chat.id
    tasks = user_scheduler.get_jobs()

    chat_tasks = [job for job in tasks if job.id.startswith(f'{chat_id}:')]
    if not chat_tasks:
        await message.edit('`No active schedules in this chat`')
        return

    result = '`Schedules in this chat:`\n\n'
    
    for index, job in enumerate(chat_tasks, 1):
        msg = job.id.split(':')[1]
        result += f'`{index}. {msg} | Interval: {job.trigger.interval}`\n\n'

    await message.edit(result, disable_web_page_preview=True)

@new_task
async def cancel_schedule(_, message):
    

user.add_handler(MessageHandler(_schedule, filters=filters.me & filters.command(*UCommand.schedule)))
user.add_handler(MessageHandler(_schedules, filters=filters.me & filters.command(*UCommand.schedulelist)))
