"""
These are the custom exceptions that I raise in the project.
"""

import discord
from discord import Integration, app_commands
from discord.ext.commands import BadArgument
from utils.database import db
from discord.ext import commands


class ItemNotFound(BadArgument):
    def __init__(self, item):
        self.item = item


class NoMoney(BadArgument):
    def __init__(self, current: int, required: int):
        self.current = current
        self.required = required

class notDev(commands.CheckFailure):
    def __str__(self, ):
        return print("You are not a developer")


class NoItem(commands.CheckFailure):
    def __init__(self, item: str):
        self.item = item

def has_item(item_name: str):
    async def predicate(ctx: commands.Context):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            raise NoItem(item_name)
        items = e.get('items', {})
        if item_name not in items:
            raise NoItem(item_name)
        return True
    return commands.check(predicate)