import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from flask import Flask
from threading import Thread

# Flask server to keep the service alive
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Configuration
API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Background Task for Channel Validation
@client.on(events.NewMessage)
async def security_handler(event):
    text = event.message.text.lower()
    if "t.me/" in text and ("join" in text or "channel" in text):
        try:
            link = [w for w in text.split() if "t.me/" in w][0]
            print(f"Detected Channel Link: {link}. Joining...")
            await client(ImportChatInviteRequest(link.split('/')[-1].replace('+', '')))
        except Exception as e:
            print(f"Auto-join error: {e}")

async def bot_logic():
    print("Bot Logic Initialized...")
    msg = os.getenv('CUSTOM_MESSAGE', "Hello!")
    link = os.getenv('LINK1')
    
    if not link:
        print("ERROR: LINK1 not found in Environment Variables!")
        return

    while True:
        try:
            print(f"Attempting to join/message: {link}")
            invite_hash = link.split('/')[-1].replace('+', '')
            
            # Join Group
            await client(ImportChatInviteRequest(invite_hash))
            await asyncio.sleep(3)
            
            # Send Message
            await client.send_message(link, msg)
            print("Message sent successfully.")
            
            # Wait 5 minutes
            await asyncio.sleep(300)
            
        except Exception as e:
            print(f"Loop error: {e}")
            await asyncio.sleep(60)

if __name__ == '__main__':
    # Start Flask in background
    Thread(target=run_flask, daemon=True).start()
    
    # Start Bot
    client.start()
    client.loop.run_until_complete(bot_logic())
