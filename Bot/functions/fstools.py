import sys
from aiofiles.os import path as aiopath
from aioshutil import rmtree as aiormtree

from Bot import user, user_scheduler, bot, bot_scheduler, logger

def get_time(seconds):
    periods = [('Day', 86400), ('Hour', 3600), ('Minute', 60), ('Second', 1)]
    result = ''
    
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if int(period_value) > 1:
                result += f'{int(period_value)} {period_name}s '
            else:
                result += f'{int(period_value)} {period_name} '
            
    return result

def exiting(signal, frame):
    try:
        if bot_scheduler:
            if bot_scheduler.running:
                bot_scheduler.shutdown(wait=False)
        if user_scheduler.running:
            user_scheduler.shutdown(wait=False)
    except:
        pass
    
    logger.info('Exiting deploy..!')
    sys.exit(0)

async def clean_download(path):
    if await aiopath.exists(path):
        logger.info(f"Cleaning Download: {path}")
        try:
            await aiormtree(path)
        except:
            pass
