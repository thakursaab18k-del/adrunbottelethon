import os
import asyncio
import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
from flask import Flask
from threading import Thread

# Logging setup (Logs se error pata chalega)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Active!"

def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

API_ID = 30089442
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'
SESSION_STRING = os.getenv('SESSION_STRING')

async def bot_logic():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    msg = os.getenv('CUSTOM_MESSAGE', "Hello!")
    
    while True:
        try:
            for i in range(1, 51):
                link = os.getenv(f'LINK{i}')
                if link:
                    try:
                        # Join
                        invite_hash = link.split('/')[-1].replace('+', '')
                        await client(ImportChatInviteRequest(invite_hash))
                        await asyncio.sleep(5)
                    except Exception as e:
                        # Agar already join hai, toh ignore karein
                        pass
                    
                    # Message
                    try:
                        await client.send_message(link, msg)
                        logging.info(f"Sent to {link}")
                    except Exception as e:
                        logging.error(f"Failed {link}: {e}")
                    
                    await asyncio.sleep(10) # Safety delay
            
            logging.info("Cycle finished. Restarting in 5 minutes...")
            await asyncio.sleep(300) # 5 min cycle
            
        except Exception as e:
            logging.error(f"Critical error: {e}")
            await asyncio.sleep(60)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(bot_logic())
