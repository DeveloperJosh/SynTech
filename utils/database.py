from hashlib import new
from mimetypes import init
import os

import pymongo
import redis
from dotenv import load_dotenv
load_dotenv()
client = pymongo.MongoClient(
    f"mongodb+srv://{os.getenv('DATABASE_NAME')}:{os.getenv('DATABASE_PASS')}@{os.getenv('DATABASE_LINK')}/cluster0?retryWrites=true&w=majority")

db = client['cluster0']

collection = db["cluster0"]
logs_collection = db["logs"]

async def set_logs(guild_id: init, channel_id: init):
    data = logs_collection.find_one({"_id": guild_id})
    if data is None:
        logs_collection.insert_one({"_id": guild_id, "channel_id": channel_id})
    else:
        return logs_collection.update_one(filter={"_id": guild_id}, update={"$set": {"channel_id": channel_id}})

########################################################################################################################

new_db = redis.Redis(host=f"{os.getenv('REDIS_HOST')}", port='13885', password=f'{os.getenv("REDIS_PASS")}')

async def connect_db_check():
    try:
        new_db.ping()
        return print("Connected to Redis")
    except:
        return print("Failed to connect to Redis")

async def warn_user(user_id: init):
    data = new_db.get(f"warns:{user_id}")
    if data is None:
        new_db.set(f"warns:{user_id}", 1)
    else:
        new_db.set(f"warns:{user_id}", int(data) + 1)

async def get_warns(user_id: init):
    data = new_db.get(f"warns:{user_id}")
    if data is None:
        return "No warns"
    else:
        return int(data)

async def clear_db():
    new_db.flushall()