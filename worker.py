import asyncio, aiohttp, time
from database import get_all, update
from pyrogram import Client
from config import *

bot=Client("worker",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)

async def check():
    async with aiohttp.ClientSession() as s:
        for u in get_all():
            url=u["url"]
            start=time.time()
            try:
                async with s.get(url,timeout=10) as r:
                    rt=round((time.time()-start)*1000)
                    status="online" if r.status==200 else "offline"
            except:
                status="offline"
                rt=-1

            if status!=u.get("status"):
                await bot.send_message(CHANNEL_ID,f"{url}\n{status} ({rt}ms)")
            update(url,status,rt)

async def main():
    await bot.start()
    while True:
        await check()
        await asyncio.sleep(30)

asyncio.run(main())
