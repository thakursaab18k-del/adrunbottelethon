import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from flask import Flask
from threading import Thread

# Flask server
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Config
API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# 1. Channel Joiner (Security Handler)
@client.on(events.NewMessage)
async def security_handler(event):
    text = event.message.text.lower()
    # Check if security bot sent a channel link
    if "t.me/" in text and ("join" in text or "channel" in text):
        try:
            link = [w for w in text.split() if "t.me/" in w][0]
            print(f"Detected Channel Link: {link}. Joining now...")
            await client(ImportChatInviteRequest(link.split('/')[-1].replace('+', '')))
            await asyncio.sleep(3)
        except Exception as e:
            print(f"Join error: {e}")

async def bot_logic():
    await client.start()
    msg = os.getenv('CUSTOM_MESSAGE', "Default message")
    
    while True:
        # Sirf pehla link (LINK1) check kar rahe hain
        link = os.getenv('LINK1')
        if not link:
            await asyncio.sleep(60)
            continue
            
        try:
            # 1. Join Group
            await client(ImportChatInviteRequest(link.split('/')[-1].replace('+', '')))
            await asyncio.sleep(2)
            
            # 2. Send Message
            print(f"Sending message to {link}")
            await client.send_message(link, msg)
            
            # 3. Wait 5 minutes
            await asyncio.sleep(300)
            
        except Exception as e:
            print(f"Cycle error: {e}")
            await asyncio.sleep(10)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    with client:
        client.loop.run_until_complete(bot_logic())
