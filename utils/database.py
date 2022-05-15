from distutils.log import error
from email import message
from hashlib import new
from mimetypes import init
import os
from redis.commands.json.path import Path

import pymongo
import redis
from dotenv import load_dotenv
import syndb
load_dotenv()
client = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv('DATABASE_NAME')}:{os.getenv('DATABASE_PASS')}@{os.getenv('DATABASE_LINK')}/cluster0?retryWrites=true&w=majority")

db = client['cluster0']
db1 = syndb.load("databases/db.json", True)

def get_starboard_messages():
    stars = db1.list_get("starboard")
    return stars

def check_db():
    ping = db1.ping()
    if ping is False:
        return print("Can't find database")
    else:
        return print("Connected to database")

collection = db["cluster0"]
logs_collection = db["logs"]

async def set_logs(guild_id: init, channel_id: init):
    data = logs_collection.find_one({"_id": guild_id})
    if data is None:
        logs_collection.insert_one({"_id": guild_id, "channel_id": channel_id})
    else:
        return logs_collection.update_one(filter={"_id": guild_id}, update={"$set": {"channel_id": channel_id}})

def check_bot_orders_db():
    data = collection.find_one({"_id": "bot_orders"})
    if data is None:
        return "No orders"
    else:
        return data