from pymongo import MongoClient
from config import MONGO_URL

db=MongoClient(MONGO_URL)["uptime_ultra"]
col=db["urls"]

def get_all():
    return list(col.find())

def add(url):
    if col.find_one({"url":url}): return False
    col.insert_one({"url":url,"status":"unknown"})
    return True

def remove(url):
    col.delete_one({"url":url})

def update(url,status,rt):
    col.update_one({"url":url},{"$set":{"status":status,"response_time":rt}})
