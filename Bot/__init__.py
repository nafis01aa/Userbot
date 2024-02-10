import os
os.system("clear|cls")

import sys
import json
import logging
from time import time, sleep
from dotenv import load_dotenv
from asyncio import create_task
from pyrogram import Client, filters, enums
from motor.motor_asyncio import AsyncIOMotorClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

all_schedulers = []

load_dotenv('config.env', override=True)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('logs.txt'), logging.StreamHandler()], level=logging.INFO)

starting_time = time()
logger = logging.getLogger(__name__)
logger.info('Starting deploy userbot...')
sleep(1)

try:
    with open('config.env', 'r') as f:
        pass
except FileNotFoundError:
    logger.error('config.env file is missing! Please check.')
    sys.exit(1)

API_ID = os.getenv('API_ID')
if not API_ID:
    logger.error('Please fill the API_ID variable in config.json file!')
    sys.exit(1)

API_HASH = os.getenv('API_HASH')
if not API_HASH:
    logger.error('Please fill the API_HASH variable in config.json file!')
    sys.exit(1)

SESSION_STRING = os.getenv('SESSION_STRING')
if not SESSION_STRING:
    logger.error('Please fill the SESSION_STRING variable in config.json file!')
    sys.exit(1)

DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR')
if not DOWNLOAD_DIR:
    DOWNLOAD_DIR = 'downloads'
else:
    if DOWNLOAD_DIR.endswith('/'):
        DOWNLOAD_DIR = DOWNLOAD_DIR.rstrip('/')

pm_hours = os.getenv('PM_HOUR')
if not pm_hours:
    pm_hours = 24 # 24 hours = one day
else:
    pm_hours = int(pm_hours)

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.warning('BOT_TOKEN variable is missing! Skipping...')
    sleep(1)

logger.info('Creating user client!')
user = Client('TGUserCli', api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING, parse_mode=enums.ParseMode.MARKDOWN).start()
user_loop = user.loop
user_name = user.me.username
user_userid = user.me.id
first_name = user.me.first_name if user.me.first_name else 'Anonymous'
last_name = user.me.last_name if user.me.last_name else ''
user_full_name = (f'{first_name} {last_name}').strip()
user_scheduler = AsyncIOScheduler(event_loop=user_loop)

if BOT_TOKEN:
    logger.info('Creating bot client!')
    bot = Client('TGUserBot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, parse_mode=enums.ParseMode.MARKDOWN).start()
    bot_loop = bot.loop
    bot_scheduler = AsyncIOScheduler(event_loop=bot_loop)
else:
    bot = ''
    bot_loop = ''
    bot_scheduler = ''

MONGODB_URL = os.getenv('MONGODB_URL')
if not MONGODB_URL:
    logger.warning('MONGODB_URL is missing! You wont get some features if you restart userbot.')
else:
    connection = AsyncIOMotorClient(MONGODB_URL)
    schedule_conn = connection.PhoenixUserbot.Scheduler
    async def get_scd():
        return [doc async for doc in schedule_conn.find({})]
    
    old_jobs = user_loop.run_until_complete(get_scd())
    for old_job in old_jobs:
        old_dict = {'_id': old_job['_id'], 'chat_id': old_job['chat_id'], 'message_id': old_job['message_id'], 'mode': old_job['mode'], 'value': old_job['value'], 'interval': old_job['interval'], 'content': old_job['content']}
        all_schedulers.append(old_dict)
