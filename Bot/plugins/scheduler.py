from asyncio import sleep
from random import randint
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from apscheduler.triggers.interval import IntervalTrigger

from Bot.utils.database import UMdb
from Bot.utils.commands import UCommand
from Bot.functions.asynctools import new_task
from Bot import user, user_scheduler, logger, all_schedulers
from Bot.functions.fstools import get_time, remove_from_old_all_schedulers

if len(all_schedulers) > 0:
    for old_scd in all_schedulers:
        user_scheduler.add_job(scheduler_task, trigger=IntervalTrigger(seconds=old_scd['interval']), (old_scd['chat_id'], old_scd['message_id']), id=old_scd['_id'])
    user_scheduler.start()

async def scheduler_task(chat_id, message_id):
    try:
        await user.copy_message(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)
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
                val = int(message.command[1].replace('s', ''))
                seconds = int(message.command[1].replace('s', ''))
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
    msg_chat_id = message.chat.id
    msg_message_id = message.reply_to_message.id
    new_shtask = user_scheduler.add_job(scheduler_task, trigger=IntervalTrigger(seconds=seconds), (msg_chat_id, msg_message_id))
    await message.edit(f'`Post scheduled for every {val} {mode}`')
    data = {'_id': new_shtask.id,'chat_id': msg_chat_id,'message_id': msg_message_id,'mode': mode,'value': val,'interval': seconds,'content': content[:10]}
    await UMdb.insert_schedule_data(data)
    all_schedulers.append(data)

@new_task
async def _schedules(_, message):
    chat_id = message.chat.id
    chat_tasks = [job for job in all_schedulers if job['chat_id'] == f'{chat_id}']
    if not chat_tasks:
        await message.edit('`No active schedules in this chat`')
        return

    result = '`Schedules in this chat:`\n\n'
    for index, job in enumerate(chat_tasks, 1):
        result += f'`{index}. {job['content']} | Interval: {job['value'] job['mode']}`\n**ID:** `{job['_id']}`\n\n'

    await message.edit(result, disable_web_page_preview=True)

@new_task
async def cancel_schedule(_, message):
    if len(message.command) < 2:
        await message.edit('`Task id not provided. Skipping..`')
        await sleep(1)
        await message.delete()
        return

    task_id = message.command[1]
    try:
        user_scheduler.remove_job(task_id)
        await UMdb.remove_schedule_data(task_id)
        await remove_from_old_all_schedulers(task_id)
        await message.edit(f'`Successfully removed this schedule task`')
        print(all_schedulers)
    except Exception as e:
        await message.edit(f'**ERROR:** `{e}`')

user.add_handler(MessageHandler(_schedule, filters=filters.me & filters.command(*UCommand.schedule)))
user.add_handler(MessageHandler(_schedules, filters=filters.me & filters.command(*UCommand.schedulelist)))
user.add_handler(MessageHandler(cancel_schedule, filters=filters.me & filters.command(*UCommand.cancelschedule)))
