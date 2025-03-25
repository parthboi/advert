#regesters a new bot....(:
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from xbothandler import create_bot_db
APP_ID = '22971136'
API_HASH = 'a7c85821da62cf7be07b6900e5992086'
print("registering a new userbot into the system..")
with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
                session_str = client.session.save()
                me = client.get_me()
                ph = me.phone
                nickname = me.first_name
                print(f"Logged in as {nickname}!")
                create_bot_db(nickname = nickname, session_string = session_str, phone_number = ph)


