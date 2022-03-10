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
slash = app_commands.CommandTree(bot)
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
    await slash.sync(guild=discord.Object(id=951303456650580058))

#This is the starting of the help command for the new slash commands
@slash.command(guild=discord.Object(id=951303456650580058), description='Test command')
async def help(interaction: discord.Interaction):
      embed = discord.Embed(title='Help', description='This is a help command', color=0x00ff00)
      await interaction.response.send_message(embed=embed)
#This is the hug command nothing really to it
@slash.command(guild=discord.Object(id=951303456650580058), description='Hug your friends')
async def hug(interaction: discord.Interaction, member: discord.Member):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/hug')
       json = await request.json()
       embed = discord.Embed(title=f"Huggies! {interaction.user.name} hugged {member.display_name}", color=MAIN_COLOR)
       embed.set_image(url=json['url'])
       await interaction.response.send_message(embed=embed)

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