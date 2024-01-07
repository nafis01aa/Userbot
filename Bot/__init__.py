# Made by Nafis
import sys
import json
import time
import logging
from pyrogram import Client, filters

try:
    with open('config.json', 'r') as f:
        configs = json.load(f)
except:
    print('Config.json file is missing! Please check.')
    sys.exit(1)

BOT_TOKEN = configs.get('BOT_TOKEN', None)
if not BOT_TOKEN:
    print('Please fill the BOT_TOKEN variable in config.json file!')
    sys.exit(1)

