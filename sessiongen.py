from pyrogram import Client, enums

api_id = int(input('Enter Your API ID:- '))
api_hash = input('Enter Your API Hash:- ')

app = Client(name='temp_ses', api_id=api_id, api_hash=api_id, in_memory=True)
app.start()

string_ = app.export_session_string()
app.send_message('me', f'**SESSION STRING FROM USERBOT:**\n\n`{string_}`', parse_mode=enums.ParseMode.MARKDOWN)
print(f'This is your session string:- \n\n{string_}')
print('\n\nAlso this string is saved in your SAVED MESSAGES section')
