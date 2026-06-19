import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from flask import Flask
from threading import Thread

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Yeh function message ke baad aane wale 'Join Channel' alerts ko handle karega
@client.on(events.NewMessage)
async def handle_security_alerts(event):
    # Agar group bot koi link bhej raha hai
    if event.message.text and ("t.me/" in event.message.text or "@" in event.message.text):
        # Check agar message mein join karne ka kaha gaya hai
        if "join" in event.message.text.lower() or "channel" in event.message.text.lower():
            try:
                # Link extract karo
                words = event.message.text.split()
                link = next((w for w in words if "t.me/" in w), None)
                if link:
                    print(f"Security Alert detected! Joining: {link}")
                    await client(ImportChatInviteRequest(link.split('/')[-1].replace('+', '')))
                    await asyncio.sleep(5)
            except Exception as e:
                print(f"Could not auto-join channel: {e}")

async def bot_logic():
    await client.start()
    msg = os.getenv('CUSTOM_MESSAGE', "Default message")
    
    while True:
        for i in range(1, 51): 
            link = os.getenv(f'LINK{i}')
            if not link: continue
            
            try:
                invite_hash = link.split('/')[-1].replace('+', '')
                await client(ImportChatInviteRequest(invite_hash))
                
                # Bot message bhejega
                print(f"Attempting to message {link}")
                await client.send_message(link, msg)
                
                # Ab 10 sec wait karein, agar message delete hua toh handler trigger hoga
                await asyncio.sleep(10)
                
            except Exception as e:
                print(f"Error: {e}")
            
            await asyncio.sleep(5)
        await asyncio.sleep(300)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    client.loop.run_until_complete(bot_logic())
