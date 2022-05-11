import discord
from discord import app_commands
from discord.ext import commands
from utils.database import db1


class Mod_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot     

    @app_commands.command()
    @app_commands.guilds(951303456650580058)
    async def get_warns(self, interaction: discord.Interaction, user: discord.User):
        data = db1.get(f"warns:{user.id}")
        if data is None:
            await interaction.response.send_message(f'{user.mention} has no warns', ephemeral=True)
        else:
            await interaction.response.send_message(f'{user.mention} has {data} warns', ephemeral=True)

    @app_commands.command()
    @app_commands.guilds(951303456650580058)
    async def warn_user(self, interaction: discord.Interaction, user: discord.User):
        data = db1.get(f"warns:{user.id}")
        if data is None:
            db1.set(f"warns:{user.id}", 1)
            await interaction.response.send_message(f'{user.mention} has 1 warn', ephemeral=True)
        else:
            db1.update(f"warns:{user.id}", int(data) + 1)
            print(data)
            await interaction.response.send_message(f'{user.mention} has {int(data) + 1} warns', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mod_Commands(bot))