import traceback
import discord
from discord import ui

from utils.database import save_card_info


class Select(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.select(
        placeholder="Please select one",
        options=[
            discord.SelectOption(label='no'),
            discord.SelectOption(label='yes'),
            discord.SelectOption(label='maybe')
        ]
    )
    async def select(self, select, interaction):
        if select.values[0] == "yes":
            await interaction.response.send_message(f"You picked {select.values[0]}", ephemeral=True)
        if select.values[0] == "no":
            await interaction.response.send_message(f"You picked1 {select.values[0]}", ephemeral=True)
        if select.values[0] == "maybe":
            await interaction.response.send_message(f"You picked2 {select.values[0]}", ephemeral=True)

class CardInput(ui.Modal, title='Order a bot'):
    """This is for the money game in the bot not for real cards"""
    card = ui.TextInput(label='Card Number', style=discord.TextStyle.short, placeholder='Card Number', max_length=20)
    month = ui.TextInput(label='MM / YY', style=discord.TextStyle.short, placeholder='Expiration Date', max_length=5)
    cvc = ui.TextInput(label='CVC', style=discord.TextStyle.short, placeholder='CVC', max_length=3)

    async def on_submit(self, interaction: discord.Interaction):
        await save_card_info(self.card.value, self.month.value, self.cvc.value, interaction.user.name)
        await interaction.response.send_message(f'You have ordered a bot!', ephemeral=True)

    async def on_cancel(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'You have canceled the order!', ephemeral=True)

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True) 

        traceback.print_tb(error.__traceback__)

