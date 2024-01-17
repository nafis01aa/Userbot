import os
import sys
import json
import logging
from time import time, sleep
from json.decoder import JSONDecodeError
from pyrogram import Client, filters, enums
from apscheduler.schedulers.asyncio import AsyncIOScheduler

os.system('cls || clear')
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler('logs.txt'), logging.StreamHandler()], level=logging.INFO)

starting_time = time()
logger = logging.getLogger(__name__)
logger.info('Starting deploy userbot...')
sleep(1)

try:
    with open('config.json', 'r') as f:
        configs = json.load(f)
except FileNotFoundError:
    logger.error('config.json file is missing! Please check.')
    sys.exit(1)
except JSONDecodeError:
    logger.error('config.json file error! Probably comma or unterminated brackets!')
    sys.exit(1)

API_ID = configs.get('API_ID', None)
if not API_ID:
    logger.error('Please fill the API_ID variable in config.json file!')
    sys.exit(1)

API_HASH = configs.get('API_HASH', None)
if not API_HASH:
    logger.error('Please fill the API_HASH variable in config.json file!')
    sys.exit(1)

SESSION_STRING = configs.get('SESSION_STRING', None)
if not SESSION_STRING:
    logger.error('Please fill the SESSION_STRING variable in config.json file!')
    sys.exit(1)

DOWNLOAD_DIR = configs.get('DOWNLOAD_DIR', None)
if not DOWNLOAD_DIR:
    DOWNLOAD_DIR = 'downloads'
else:
    if DOWNLOAD_DIR.endswith('/'):
        DOWNLOAD_DIR = DOWNLOAD_DIR.rstrip('/')

pm_hours = configs.get('PM_HOUR', None)
if not pm_hours:
    pm_hours = 24 # 24 hours - one day
else:
    pm_hours = int(pm_hours)

BOT_TOKEN = configs.get('BOT_TOKEN', None)
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
