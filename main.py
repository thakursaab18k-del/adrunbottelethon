import os
import asyncio
import random
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from flask import Flask
from threading import Thread

# Flask server setup
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Config
API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

async def bot_logic():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    msg = os.getenv('CUSTOM_MESSAGE', "Default message")
    
    while True:
        for i in range(1, 51): 
            link = os.getenv(f'LINK{i}')
            if link:
                try:
                    # 1. Join Attempt
                    invite_hash = link.split('/')[-1].replace('+', '')
                    print(f"Joining {link}...")
                    await client(ImportChatInviteRequest(invite_hash))
                    
                    # 2. SECURITY PAUSE: Channel join/Captcha ke liye 15 sec wait
                    print("Security wait for Channel/Captcha validation...")
                    await asyncio.sleep(15) 
                    
                    # 3. Message Delivery
                    # Random delay to look like a human
                    await asyncio.sleep(random.randint(5, 10))
                    await client.send_message(link, msg)
                    print(f"Message delivered to {link}")
                    
                except Exception as e:
                    # Agar pehle se member hain, toh seedha message try karein
                    if "already in the chat" in str(e).lower():
                        await client.send_message(link, msg)
                    else:
                        print(f"Skipping/Issue with {link}: {e}")
                
                await asyncio.sleep(10) # Next group se pehle pause
        
        await asyncio.sleep(300) # Full cycle ke baad 5 min ka break

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(bot_logic())
