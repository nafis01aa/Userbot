from pyrogram import Client, enums

api_id = int(input('Enter Your API ID:- '))
api_hash = input('Enter Your API Hash:- ')
phone_number = input('Enter Your Phone Number [With Country Code] :- ')

app = Client('temporary_session', api_id, api_hash, phone_number=phone_number, in_memory=True)
app.start()

string_ = app.export_session_string()
app.send_message('me', f'**SESSION STRING FROM USERBOT:**\n\n`{string_}`', parse_mode=enums.ParseMode.MARKDOWN)
print(f'This is your session string:- \n\n{string_}')
print('\n\nAlso this string is saved in your SAVED MESSAGES section')
