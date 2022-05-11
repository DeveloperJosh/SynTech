import logging
import os

import discord
from discord.ext import commands
from importlib_metadata import files

from config import PREFIXES, DEVELOPERS
from utils.database import check_db

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    owner_ids=DEVELOPERS,
    activity=discord.Game(name="/help"),
    command_prefix=PREFIXES,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True),
    strip_after_prefix=True
)
logging.basicConfig(level=logging.INFO)


async def load_cogs():
    i = 0
    files = os.listdir('./cogs')
    for file in files:
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
            i += 1
    logging.info(f"Loaded {i} cogs from \"cogs\"")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv('DISCORD_BOT_SECRET'), reconnect=True)

@bot.event
async def on_ready():
    print("""

░██████╗██╗░░░██╗███╗░░██╗████████╗███████╗░█████╗░██╗░░██╗
██╔════╝╚██╗░██╔╝████╗░██║╚══██╔══╝██╔════╝██╔══██╗██║░░██║
╚█████╗░░╚████╔╝░██╔██╗██║░░░██║░░░█████╗░░██║░░╚═╝███████║
██████╔╝░░░██║░░░██║░╚███║░░░██║░░░███████╗╚█████╔╝██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝░░░╚═╝░░░╚══════╝░╚════╝░╚═╝░░╚═╝
        """)
    print(f"Logged in as {bot.user}")
    print(f"Connected to: {len(bot.guilds)} guilds")
    print(f"Connected to: {len(bot.users)} users")
    print(f"Connected to: {len(bot.cogs)} cogs")
    print(f"Connected to: {len(bot.commands)} commands")
    print(f"Connected to: {len(bot.emojis)} emojis")
    print(f"Connected to: {len(bot.voice_clients)} voice clients")
    print(f"Connected to: {len(bot.private_channels)} private_channels")
    check_db()
    await bot.tree.sync(guild=discord.Object(id=951303456650580058))
