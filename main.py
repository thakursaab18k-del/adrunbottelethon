import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from flask import Flask
from threading import Thread

# Flask for Render Port
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"

def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Config
API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = '1BVtsOLYBu4ZRdrl7JNhMqSyOfR0w-DCd-KDRm7qFOXsfQfH362n2Sgag3F__QWwXZUiwnxt8f-UXAY6A5lEJAJc4B55odBQU-870m-IK8OkCYeNsVSupK1XqQjK_m72Hb1vLIXLo00y4DLVCbGOgGrG6z0HGAO1Vr-Mxcr19k5SIVkX3gF8AyMKrr9YTXAHRxHXBDgBSmDEhDsjd4EI99xL3OsPdEBrLDsle0xxsOiRm_sBapkW4UfGsNXNG1dE0j0kVfgN8q7nqCUqOGmZEEFoNYWhkjICKFtJoQ6d79SKEOaJ7ohj2q7nlashMELWRJaWvBjXaELxMMISLyH8vO1EkFFxAU7A='

async def bot_logic():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    
    links_raw = os.getenv('GROUP_LINKS', '')
    msg = os.getenv('CUSTOM_MESSAGE', "Default Message")
    groups = [l.strip() for l in links_raw.split(',') if l.strip()]

    while True:
        for link in groups:
            try:
                # 1. Join attempt
                await client(JoinChannelRequest(link))
                print(f"Successfully joined: {link}")
                
                # 2. Send Message
                await client.send_message(link, msg)
                print(f"Message sent to {link}")
                
            except Exception as e:
                print(f"Skipping {link} due to error: {e}")
                continue # Yeh line bahut zaroori hai, ye bot ko agle group par bhej degi
            
            await asyncio.sleep(15) # Har group ke beech 15 seconds ka gap
            
        print("Cycle complete. Waiting for next run.")
        await asyncio.sleep(1800) # 30 minute wait

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(bot_logic())
