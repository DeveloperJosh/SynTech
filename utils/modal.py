import traceback
from turtle import title
from unicodedata import name
import discord
from discord import ui

class Ban(ui.Modal, title='Ban a user'):
    user = ui.TextInput(label='User ID', style=discord.TextStyle.short, placeholder='User ID', max_length=20)
    reason = ui.TextInput(label='Reason', style=discord.TextStyle.short, placeholder='Reason', max_length=20)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.guild.ban(discord.Object(id=self.user.value), reason=self.reason.value)
        await interaction.response.send_message(f'You have banned {self.user.value}!', ephemeral=True)
    async def on_cancel(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You have canceled the ban!', ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True) 

        traceback.print_tb(error.__traceback__)