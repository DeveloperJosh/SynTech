import asyncio
from distutils.log import error
import logging
import os

import discord
from discord.ext import commands, tasks

from config import MAIN_COLOR, PREFIXES, DEVELOPERS, COGS

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    owner_ids=DEVELOPERS,
    command_prefix=PREFIXES,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True),
    strip_after_prefix=True
)
logging.basicConfig(level=logging.INFO)

# This is our new way to load cogs and load the bot
async def main():
    async with bot:
        for ext in COGS:
            await bot.load_extension(ext)
        await bot.start(os.getenv('DISCORD_BOT_SECRET'))

def check_cogs(self):
    for ext in COGS:
        if not ext in self.bot.extensions:
            error(f'{ext} is not loaded')


@bot.event
async def on_ready():
    print("""

░██████╗██╗░░░██╗███╗░░██╗████████╗███████╗░█████╗░██╗░░██╗
██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔════╝██╔══██╗██║░░██║
╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░█████╗░░██║░░╚═╝███████║
░╚═══██╗░░╚██╔╝░░██║╚████║░░░██║░░░██╔══╝░░██║░░██╗██╔══██║
██████╔╝░░░██║░░░██║░╚███║░░░██║░░░███████╗╚█████╔╝██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚═╝
        """)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
    await bot.tree.sync(guild=discord.Object(id=951303456650580058))