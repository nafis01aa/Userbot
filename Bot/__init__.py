# Made by Nafis

import sys
import time
import logging
from pyrogram import Client, filters

try:
    with open('config.json', 'r') as f:
        configs = f.read()
except:
    print('Config.json file is missing! Please check.')
    sys.exit(1)

