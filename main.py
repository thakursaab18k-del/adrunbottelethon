import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from flask import Flask
from threading import Thread

# Flask server
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running and attempting to join groups!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

async def bot_logic():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    msg = os.getenv('CUSTOM_MESSAGE', "Default message")
    
    while True:
        print("Checking groups...")
        for i in range(1, 51): 
            link = os.getenv(f'LINK{i}')
            if link:
                try:
                    # 1. Pehle check karein agar hum already member hain
                    try:
                        await client.get_entity(link)
                        print(f"Already a member of {link}")
                    except:
                        # 2. Agar member nahi hain, toh join karein
                        print(f"Attempting to join {link}...")
                        invite_hash = link.split('/')[-1].replace('+', '')
                        await client(ImportChatInviteRequest(invite_hash))
                        print(f"Successfully joined {link}")
                        await asyncio.sleep(10) # Join karne ke baad thoda rest

                    # 3. Message bhejein
                    await client.send_message(link, msg)
                    print(f"Message sent to {link}")
                    
                except Exception as e:
                    print(f"Issue with {link}: {e}")
                
                await asyncio.sleep(60) # Har group ke baad 1 minute ka gap (Safety First!)
        
        print("Cycle done. Sleeping for 1 hour before next run.")
        await asyncio.sleep(3600)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(bot_logic())
