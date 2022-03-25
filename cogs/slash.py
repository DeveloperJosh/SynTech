from cgitb import text
import io
import logging
from pyexpat import model
from turtle import title
import discord
import aiohttp
import random
from discord.ext import commands
from discord import app_commands
from utils.select import CardInput

from config import FUN_COLOR, MAIN_COLOR
from utils.embeds import custom_embed
### Added slash commands to the new cogs folder

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Slash is ready')

    @app_commands.command(description="test command")
    @app_commands.guilds(951303456650580058)
    async def help(self, interaction: discord.Interaction):
      embed = discord.Embed(title='Help', description='This is a help command', color=0x00ff00)
      await interaction.response.send_message(embed=embed)

    @app_commands.command(description="For hugging your friends")
    @app_commands.guilds(951303456650580058)
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
       async with aiohttp.ClientSession() as session:
        request = await session.get('https://nekos.life/api/v2/img/hug')
        json = await request.json()
        embed = discord.Embed(title=f"Huggies! {interaction.user.name} hugged {member.display_name}", color=MAIN_COLOR)
        embed.set_image(url=json['url'])
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="For kissing your lovers or friends")
    @app_commands.guilds(951303456650580058)
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
         async with aiohttp.ClientSession() as session:
          request = await session.get('https://nekos.life/api/v2/img/kiss')
          json = await request.json()
          embed = discord.Embed(title=f"Kisses! {interaction.user.name} kissed {member.display_name}", color=MAIN_COLOR)
          embed.set_image(url=json['url'])
          await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Gay Power")
    @app_commands.guilds(951303456650580058)
    async def gay(self, interaction: discord.Interaction, member: discord.Member):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.replace(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gay.png")
                    em = discord.Embed(
                        title="He has came out",
                        color=MAIN_COLOR,
                    )
                    em.set_image(url="attachment://gay.png")
                    await interaction.response.send_message(embed=em, file=file)
                else:
                     await interaction.response.send_message('No gay :(')
        await session.close()

    @app_commands.command(name="8ball", description="For cuddling your friends")
    @app_commands.guilds(951303456650580058)
    async def _8ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        response = random.choice(responses)
        embed = discord.Embed(title="8ball", description=f"Question: {question}\nAnswer: {response}", color=FUN_COLOR)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="making an embed")
    @app_commands.guilds(951303456650580058)
    @app_commands.describe(title='Adding a title to the embed')
    @app_commands.describe(text='Adding a description to the embed')
    async def embed(self, interaction: discord.Interaction, title: str, text: str):
        embed = custom_embed(title=title, description=text)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="For ordering a bot")
    @app_commands.guilds(951303456650580058)
    async def buy(self, interaction: discord.Interaction):
     print(interaction.user.name)
     await interaction.response.send_modal(CardInput())
  
async def setup(bot):
    await bot.add_cog(Slash(bot))