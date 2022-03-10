import logging
import os
import aiohttp

import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.help import MyHelp
from utils.database import db
from discord import app_commands

from config import MAIN_COLOR, PREFIXES, DEVELOPERS

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.AutoShardedBot(
    owner_ids=DEVELOPERS,
    command_prefix=PREFIXES,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True),
    strip_after_prefix=True
)
##tree = app_commands.CommandTree(bot)
logging.basicConfig(level=logging.INFO)
bot.load_extension('jishaku')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    logging.info(' __________________________________________________ ')
    logging.info('|                                                  |')
    logging.info('|                 Bot has Started                  |')
    logging.info('|                                                  |')
    logging.info('+__________________________________________________+')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help"))

@bot.event
async def on_message(message):
    e = db.collection.find_one({"user": message.author.id})

    if e is None:
        await bot.process_commands(message)
    else:
        return

load_dotenv('.env')

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_SECRET'))