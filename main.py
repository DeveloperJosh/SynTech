import asyncio
import logging
import os

import discord
from discord.ext import commands

from config import MAIN_COLOR, PREFIXES, DEVELOPERS

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
cogs = ['cogs.help', 'cogs.moderation', 'cogs.slash', 'cogs.money', 'cogs.general', 'cogs.ticket', 'cogs.images', 'cogs.error_handling', 'cogs.nsfw', 'cogs.owners']
logging.basicConfig(level=logging.INFO)

# This is our new way to load cogs and load the bot
async def main():
    async with bot:
        for ext in cogs:
            await bot.load_extension(ext)
        await bot.start(os.getenv('DISCORD_BOT_SECRET'))


@bot.event
async def on_ready():
    logging.info(' __________________________________________________ ')
    logging.info('|                                                  |')
    logging.info('|                 Bot has Started                  |')
    logging.info('|                                                  |')
    logging.info('+__________________________________________________+')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help"))
    await bot.tree.sync(guild=discord.Object(id=951303456650580058))

asyncio.run(main())