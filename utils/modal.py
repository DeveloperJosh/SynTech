import traceback
from turtle import title
import discord
from discord import ui

from utils.database import save_card_info


class CardInput(ui.Modal, title='Order a bot'):
    """This is for the money game in the bot not for real cards"""
    card = ui.TextInput(label='Card Number', style=discord.TextStyle.short, placeholder='Card Number', max_length=20)
    month = ui.TextInput(label='MM / YY', style=discord.TextStyle.short, placeholder='Expiration Date', max_length=5)
    cvc = ui.TextInput(label='CVC', style=discord.TextStyle.short, placeholder='CVC', max_length=3)

    async def on_submit(self, interaction: discord.Interaction):
        await save_card_info(self.card.value, self.month.value, self.cvc.value, interaction.user.name)
        await interaction.response.send_message(f'You have ordered a card!', ephemeral=True)
    async def on_cancel(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You have canceled the order!', ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True) 

        traceback.print_tb(error.__traceback__)

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