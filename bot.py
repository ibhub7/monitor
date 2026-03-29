import os
import asyncio
from pyrogram import Client, filters, idle
from aiohttp import web
from database import add, remove
from config import *

# --- CONFIG ---
ADMINS = [123456789]
PORT = int(os.environ.get("PORT", 8080)) # Koyeb provides this automatically

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- HEALTH CHECK SERVER ---
async def handle_health(request):
    return web.Response(text="Bot is Alive!")

async def start_web_server():
    server = web.Application()
    server.router.add_get("/", handle_health)
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"✅ Web server started on port {PORT}")

# --- BOT COMMANDS ---
@app.on_message(filters.command("addurl") & filters.user(ADMINS))
async def addurl(_, m):
    if len(m.command) < 2:
        return await m.reply("Usage: /addurl <url>")
    url = m.text.split(" ", 1)[1]
    await m.reply("✅ Added" if add(url) else "❌ Already Exists")

@app.on_message(filters.command("removeurl") & filters.user(ADMINS))
async def rem(_, m):
    if len(m.command) < 2:
        return await m.reply("Usage: /removeurl <url>")
    url = m.text.split(" ", 1)[1]
    remove(url)
    await m.reply("🗑 Removed")

# --- MAIN RUNNER ---
async def main():
    # 1. Start the health check server first
    await start_web_server()
    
    # 2. Start the Pyrogram client
    await app.start()
    print("🤖 Bot is starting...")
    
    # 3. Keep the bot running
    await idle()
    
    # 4. Stop the bot gracefully when done
    await app.stop()

if __name__ == "__main__":
    # Use the asyncio event loop to run everything
    asyncio.get_event_loop().run_until_complete(main())
