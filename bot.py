from pyrogram import Client, filters
from database import add, remove
from config import *

ADMINS=[123456789]

app=Client("bot",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)

@app.on_message(filters.command("addurl") & filters.user(ADMINS))
async def addurl(_,m):
    url=m.text.split(" ",1)[1]
    await m.reply("Added" if add(url) else "Exists")

@app.on_message(filters.command("removeurl") & filters.user(ADMINS))
async def rem(_,m):
    url=m.text.split(" ",1)[1]
    remove(url)
    await m.reply("Removed")

app.run()
