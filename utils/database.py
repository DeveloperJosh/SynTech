from mimetypes import init
import os

import pymongo
from dotenv import load_dotenv

load_dotenv('.env')
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