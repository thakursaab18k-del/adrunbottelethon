import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from flask import Flask
from threading import Thread

# Flask server to keep the service "Live" on Render
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is active!"

def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# API Config
API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

async def bot_logic():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    
    msg = os.getenv('CUSTOM_MESSAGE', "Default message")
    
    while True:
        print("Starting new broadcast cycle...")
        # Check for LINK1 to LINK50
        for i in range(1, 51): 
            link = os.getenv(f'LINK{i}')
            if link:
                try:
                    await client(JoinChannelRequest(link))
                    await client.send_message(link, msg)
                    print(f"Success: Sent to {link}")
                    await asyncio.sleep(20) # 20 seconds gap between groups
                except Exception as e:
                    print(f"Skipped {link}: {e}")
        
        print("Cycle complete. Waiting for next run.")
        await asyncio.sleep(300) # 5 minute sleep (Adjust this as needed)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(bot_logic())
