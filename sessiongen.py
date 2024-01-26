from os import system
from time import time

try:
    from pyrogram import Client, enums
except ModuleNotFoundError:
    print('Pyrogram package not found. Installing...')
    
    try:
        system('pip install pyrogram > nul 2>&1')
        print('Pyrogram installed successfully!\n\n')
        from pyrogram import Client, enums
    except Exception as e:
        print(f'Error installing Pyrogram: {e}')
        exit(1)
except OSError as e:
    try:
        system('pip3 install pyrogram > nul 2>&1')
        print('Pyrogram installed successfully!\n\n')
        from pyrogram import Client, enums
    except Exception as e:
        print(f'Error installing Pyrogram: {e}')
        exit(1)

api_id = input("Enter Your API ID: ")
api_hash = input("Enter Your API HASH: ")
phone_number = input("Enter Your Phone Number (With Country Code): ")

user = Client(f"temporary_{time()}_{time()}", api_id, api_hash, phone_number=phone_number, in_memory=True).start()

session_string = user.export_session_string()
print(f"Your Session String is:\n\n{session_string}")

user.send_message('me', f'**SESSION STRING FROM USERBOT:**\n\n`{session_string}`', parse_mode=enums.ParseMode.MARKDOWN)
print('\n\nAlso this string is saved in your SAVED MESSAGES section')
