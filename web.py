from fastapi import FastAPI, WebSocket
from database import get_all
import asyncio

app=FastAPI()

@app.get("/")
def home():
    return {"status":"running"}

@app.websocket("/ws")
async def ws(ws:WebSocket):
    await ws.accept()
    while True:
        await ws.send_json(get_all())
        await asyncio.sleep(2)
