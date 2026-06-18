import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# ==================== CONFIGURATION ====================
API_ID = 30089442                  
API_HASH = '842dc7bbd3ce4a4f96194814dcb725a8'   

# Your generated session key
SESSION_STRING = '1BVtsOLYBu4ZRdrl7JNhMqSyOfR0w-DCd-KDRm7qFOXsfQfH362n2Sgag3F__QWwXZUiwnxt8f-UXAY6A5lEJAJc4B55odBQU-870m-IK8OkCYeNsVSupK1XqQjK_m72Hb1vLIXLo00y4DLVCbGOgGrG6z0HGAO1Vr-Mxcr19k5SIVkX3gF8AyMKrr9YTXAHRxHXBDgBSmDEhDsjd4EI99xL3OsPdEBrLDsle0xxsOiRm_sBapkW4UfGsNXNG1dE0j0kVfgN8q7nqCUqOGmZEEFoNYWhkjICKFtJoQ6d79SKEOaJ7ohj2q7nlashMELWRJaWvBjXaELxMMISLyH8vO1EkFFxAU7A=' 

# This line checks Render's Environment Variables for "CUSTOM_MESSAGE"
# If it doesn't find it, it defaults to the text below.
CUSTOM_MESSAGE = os.getenv('CUSTOM_MESSAGE', "Default message: Hello from my cloud bot!")
INTERVAL_SECONDS = 300  # 5 minutes
# =======================================================

async def main():
    print("Connecting to Telegram via saved session...")
    async with TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH) as client:
        print("Successfully connected as your user account!")
        
        while True:
            try:
                # This sends the text/links straight to your "Saved Messages" chat
                await client.send_message('me', CUSTOM_MESSAGE)
                print(f"Message sent to Saved Messages! Sleeping for {INTERVAL_SECONDS} seconds...")
            except Exception as e:
                print(f"An error occurred: {e}")
            
            await asyncio.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    asyncio.run(main())
