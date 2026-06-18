import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

# ==================== CONFIGURATION ====================
# 1. Get these from https://my.telegram.org
API_ID = 1234567                  # Replace with your numeric API ID
API_HASH = 'your_api_hash_here'   # Replace with your API Hash string

# 2. Generate this locally on your PC first (See previous steps)
SESSION_STRING = 'PASTE_YOUR_STRING_SESSION_HERE' 

# 3. Customize your message here
CUSTOM_MESSAGE = "This is my customized message sent automatically every 5 minutes!"

# 4. Set the timer interval (300 seconds = 5 minutes)
INTERVAL_SECONDS = 300  
# =======================================================

# Track the groups you want to broadcast to
target_groups = set()

# Initialize the Telethon Userbot client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# --- BACKGROUND LOOP: SENDS MESSAGES EVERY 5 MINUTES ---
async def message_broadcaster():
    await client.start()
    print("🚀 5-minute broadcasting loop has started running...")
    
    while True:
        # Wait for 5 minutes before checking/sending messages
        await asyncio.sleep(INTERVAL_SECONDS)
        
        if not target_groups:
            print("⏳ Waiting for you to send group links to Saved Messages...")
            continue
            
        print(f"🔄 Starting broadcast cycle to {len(target_groups)} groups...")
        
        # Loop through all the groups you added
        for group_id in list(target_groups):
            try:
                await client.send_message(group_id, CUSTOM_MESSAGE)
                print(f"✅ Message sent successfully to Group ID: {group_id}")
                # Anti-flood delay: waits 3 seconds between different groups so Telegram doesn't crash
                await asyncio.sleep(3) 
            except Exception as e:
                print(f"❌ Could not send message to group {group_id}: {e}")

# --- EVENT LISTENER: WATCHES YOUR SAVED MESSAGES FOR LINKS ---
@client.on(events.NewMessage(chats='me'))
async def handle_new_links(event):
    text = event.raw_text
    
    # Regex to find any Telegram links (t.me/... or telegram.me/...)
    links = re.findall(r'(?:https?://)?(?:t\.me|telegram\.me)/(joinchat/|\+)?([\w-]+)', text)
    
    for type_prefix, group_identifier in links:
        try:
            print(f"🔍 Processing link payload: {group_identifier}")
            
            # Case A: It is a private invite link (contains 'joinchat/' or '+')
            if type_prefix:  
                updates = await client(ImportChatInviteRequest(group_identifier))
                chat = updates.chats[0]
            # Case B: It is a public group username
            else:  
                chat = await client.get_entity(group_identifier)
                await client(JoinChannelRequest(chat))
                
            print(f"🎉 Successfully joined: {chat.title}")
            target_groups.add(chat.id)
            await event.reply(f"🎯 **Joined & Added to 5-min Loop:** {chat.title}")
            
            # --- AUTO-JOIN "REQUIRED CHANNELS" COMPLIANCE ---
            await asyncio.sleep(2) # Wait for verification bots to post
            async for msg in client.iter_messages(chat, limit=5):
                if msg.text and ("join" in msg.text.lower() or "channel" in msg.text.lower()):
                    sub_links = re.findall(r'(?:https?://)?(?:t\.me|telegram\.me)/([\w]+)', msg.text)
                    for channel_username in sub_links:
                        try:
                            channel_entity = await client.get_entity(channel_username)
                            await client(JoinChannelRequest(channel_entity))
                            print(f"🤖 Auto-joined requirement channel: @{channel_username}")
                            await event.reply(f"🔗 **Auto-joined required verification channel:** @{channel_username}")
                        except Exception:
                            pass 
                            
        except Exception as e:
            await event.reply(f"⚠️ **Error processing link:** `{group_identifier}`\nReason: {str(e)}")

# --- START BOTH CODE ROUTINES ---
if __name__ == '__main__':
    # Add the broadcasting loop task to run alongside the event listener
    client.loop.create_task(message_broadcaster())
    
    print("⚡ Userbot is online! Ready to accept links in Saved Messages.")
    # Keep the userbot active
    client.run_until_disconnected()
