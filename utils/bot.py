import logging
import os

import discord
from discord.ext import commands

from config import PREFIXES, DEVELOPERS, COGS

intents = discord.Intents.default()
intents.members = True

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

@bot.event
async def on_ready():
    os.system('cls')
    print("""

░██████╗██╗░░░██╗███╗░░██╗████████╗███████╗░█████╗░██╗░░██╗
██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔════╝██╔══██╗██║░░██║
╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░█████╗░░██║░░╚═╝███████║
██████╔╝░░░██║░░░██║░╚███║░░░██║░░░███████╗╚█████╔╝██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚═╝
        """)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
    await bot.tree.sync(guild=discord.Object(id=951303456650580058))