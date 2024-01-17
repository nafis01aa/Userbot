from aiofiles.os import path as aiopath
from aioshutil import rmtree as aiormtree

from Bot import user, bot, logger

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

async def clean_download(path):
    if await aiopath.exists(path):
        logger.info(f"Cleaning Download: {path}")
        try:
            await aiormtree(path)
        except:
            pass
