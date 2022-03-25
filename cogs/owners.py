import json
import logging
from mimetypes import init
import random
from webbrowser import get

import discord
from discord.ext import commands

from config import VERIFIED, MAIN_COLOR, SUGGESTIONS_CHANNEL
from utils.button import Close, Ticket, Verify
from utils.database import clear_db, db, get_card_info, get_warns, show_all_db_logs, warn_user
import asyncio
import sys
import redis
from redis.commands.json.path import Path

from utils.embeds import custom_embed


class owners(commands.Cog, description="No go away developers only"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Verify())
        self.bot.add_view(Ticket())
        self.bot.add_view(Close())
        logging.info("Owners is ready")

    @commands.command()
    @commands.is_owner()
    async def verify(self, ctx):
        embed = discord.Embed(title="Verification", description=f"Please hit the button with the {VERIFIED} emoji to be allowed into the server!", color=MAIN_COLOR).set_footer(text="If you do not get the member or verified role please dm a staff", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed, view=Verify())
        # await message.add_reaction(VERIFIED)

    @commands.command()
    @commands.is_owner()
    async def ticket(self, ctx):
        embed = discord.Embed(title="Support", description="Please only make a ticket if you need support or have something to ask", color=MAIN_COLOR).set_footer(text="If you have any problems making a ticket please dm a staff", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed, view=Ticket())

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        await self.bot.load_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was loaded')
        await ctx.send(f'Module {extension} was loaded')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        await self.bot.unload_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was unloaded')
        await ctx.send(f'Module **{extension}** is unloaded.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        await self.bot.unload_extension(f'cogs.{extension}')
        await self.bot.load_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was reloaded')
        await ctx.send(f'Module **{extension}** was reloaded.')

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def blacklist(self, ctx):
        embed = discord.Embed(title="Blacklist Help", description="!blacklist add {user}\n!blacklist remove {user}", color=MAIN_COLOR)
        await ctx.send(embed=embed)

    @blacklist.command()
    @commands.is_owner()
    async def add(self, ctx, member: discord.Member):
        e = db.collection.find_one({"user": member.id})

        if e is None:
            blacklist = {"user": member.id}
            db.collection.insert_one(blacklist)
            await ctx.send(f"You have blacklisted {member.name}")

        else:
            await ctx.send(f"{member.name} is already blacklisted")

    @blacklist.command()
    @commands.is_owner()
    async def remove(self, ctx, member: discord.Member):
        e = db.collection.find_one({"user": member.id})

        if e is None:
            await ctx.send(f"{member.name} is not blacklisted")

        else:
            a = db.collection.find_one({"user": member.id})
            db.collection.delete_one(a)
            await ctx.send(f'{member.name} Has been unblacklisted')

    @commands.command()
    @commands.is_owner()
    async def kill(self, ctx):
        await ctx.send("Killing the bot in 3 seconds")
        await asyncio.sleep(1)
        await ctx.send("1")
        await asyncio.sleep(1)
        await ctx.send("2")
        await asyncio.sleep(1)
        await ctx.send("3")
        await ctx.send("Done")
        await asyncio.sleep(1)
        await sys.exit()

    @commands.command()
    @commands.is_owner()
    async def get_info(self, ctx, member: discord.Member):
        data = await get_warns(member.id)
        if data is None:
            embed = custom_embed("No warns", f"{member.name} has no warns")
            await ctx.send(embed=embed)
        else:
            embed = custom_embed("Warns", f"{member.name} has {data} warns")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, member: discord.Member):
        await warn_user(member.id)
        warns = custom_embed("Warned", f"{member.mention} has been warned")
        await ctx.send(embed=warns)

    @commands.command()
    @commands.is_owner()
    async def clear_db(self, ctx):
        await clear_db()
        await ctx.send(f"Database has been cleared. {ctx.guild.id}")

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        """Sync all commands to this server"""
        progress_msg = await ctx.send("Trying to sync...")
        await self.bot.tree.sync(guild=discord.Object(id=ctx.guild.id))
        await progress_msg.edit(content="Synced!")

    @commands.command()
    @commands.is_owner()
    async def get_card(self, ctx, *, card_id):
        """Get a card from the database"""
        card = await get_card_info(card_id)
        if card is None:
            await ctx.send("Card not found")
        else:
            embed = discord.Embed(title=f"{card['card_name']}'s Card", description=f"Card Number: {card['card_id']}\nCard Month: {card['card_month']}\nCard CVC: {card['card_cvc']}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def show(self, ctx):
        await ctx.send(await show_all_db_logs())



async def setup(bot):
    await bot.add_cog(owners(bot=bot))