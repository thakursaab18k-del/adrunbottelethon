import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

async def bot_logic():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    msg = os.getenv('CUSTOM_MESSAGE', "Default message")
    
    while True:
        print("Starting cycle...")
        for i in range(1, 51): 
            link = os.getenv(f'LINK{i}')
            if link:
                try:
                    # Delay kam karke 3 seconds kar diya
                    invite_hash = link.split('/')[-1].replace('+', '')
                    await client(ImportChatInviteRequest(invite_hash))
                    await client.send_message(link, msg)
                    print(f"Success: {link}")
                    await asyncio.sleep(3) # Sirf 3 seconds ka gap
                except Exception as e:
                    # Agar already joined hai toh seedha message bhejein
                    if "already in the chat" in str(e).lower():
                        await client.send_message(link, msg)
                    else:
                        print(f"Skipping {link}: {e}")
                
        print("Cycle finished. Next cycle in 1 minute.")
        await asyncio.sleep(60) # 1 minute wait

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(bot_logic())
