from pyrogram import Client, enums

api_id = input("Enter Your API ID: ")

api_hash = input("Enter Your API HASH: ")

phone_number = input("Enter Your Phone Number: ")

user = Client("temporary", api_id, api_hash, phone_number=phone_number, in_memory=True)

user.start()

session_string = user.export_session_string()

print(f"Your Session String is:\n\n{session_string}")

user.send_message('me', f'**SESSION STRING FROM USERBOT:**\n\n`{session_string}`', parse_mode=enums.ParseMode.MARKDOWN)

print('\n\nAlso this string is saved in your SAVED MESSAGES section')
