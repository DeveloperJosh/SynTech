import logging
import random
import discord

from discord.ext import commands
from typing import Optional, Union
from config import EMOJIS_FOR_COGS, MAIN_COLOR, MONEY_EMOJI
from utils.database import db
from utils.constants import items
from utils.converters import ItemConverter
from utils.classes import Item
from utils.exceptions import NoMoney, has_item
from utils.button import LeaderboardView, Search


class money(commands.Cog, description="Make money then sleep"):
    def __init__(self, bot):
        self.bot = bot
        self.items = items

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Money is ready')

    @commands.command(help="See what you can buy", name="shop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _shop(self, ctx: commands.Context):
        embed = discord.Embed(
            title=f"Shop [{len(self.items)}]",
            description="Here's what you can buy",
            colour=MAIN_COLOR,
        ).set_footer(text=f"Use {ctx.clean_prefix}buy <item> to buy an item!")
        for item, stuff in self.items.items():
            embed.add_field(
                name=f"{stuff['emoji']} • {item.title()}",
                value=f"""
**Prize:** {EMOJIS_FOR_COGS['money']} {stuff['prize']}
**Description:** {stuff['description']}
                """
            )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.member)
    async def work(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            number = random.randint(50, 200)
            responses = ['Coder', "PornStar", "EpicBot Dev", "Dog Walker"]
            jobs = random.choice(responses)
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Work", description=f"You worked as a {jobs} for {MONEY_EMOJI} {number}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        else:
            money_number = random.randint(50, 200)
            responses = ['Coder', "PornStar", "EpicBot Dev", "Dog Walker"]
            jobs = random.choice(responses)
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + money_number, "bank": e['bank']}})
            embed = discord.Embed(title="Work", description=f"You worked as a {jobs} for {MONEY_EMOJI} {money_number}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command(aliases=['deposit', 'dep'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def transfer(self, ctx, money_stuff: Union[int, str]):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})

        if money_stuff == "all":
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] - e['money'], "bank": e['bank'] + e['money']}})
            embed = discord.Embed(title="Transfer", description=f"All of your {MONEY_EMOJI} was moved to your bank account", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif money_stuff == "max":
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] - e['money'], "bank": e['bank'] + e['money']}})
            embed = discord.Embed(title="Transfer", description=f"All of your {MONEY_EMOJI} was moved to your bank account", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e is None:
            ctx.send("No money lol")

        elif e['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        elif e['money'] >= money_stuff:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] - money_stuff, "bank": e['bank'] + money_stuff}})
            embed = discord.Embed(title="Transfer", description=f"{MONEY_EMOJI} {money_stuff} to your bank account", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            await ctx.send("You don't have enough money")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, money_stuff: Union[int, str]):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})

        if money_stuff == "all":
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + e['bank'], "bank": e['bank'] - e['bank']}})
            embed = discord.Embed(title="Withdraw", description=f"All of your {MONEY_EMOJI} was put into your wallet", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif money_stuff == "max":
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + e['bank'], "bank": e['bank'] - e['bank']}})
            embed = discord.Embed(title="Withdraw", description=f"All of your {MONEY_EMOJI} was put into your wallet", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e is None:
            ctx.send("No money lol")

        elif e['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        elif e['bank'] >= money_stuff:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + money_stuff, "bank": e['bank'] - money_stuff}})
            embed = discord.Embed(title="Withdraw", description=f"{MONEY_EMOJI} {money_stuff} to your wallet", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            await ctx.send("You don't have enough money")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def rob(self, ctx, member: discord.Member = None):
        a = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        number = 20

        if member is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("Please ping a user")
            return

        elif member == ctx.author:
            await ctx.send("Please ping a user")
            return

        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": member.id})

        if a is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("Please open a account by running `!work`")
            return

        elif a['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        if e['money'] >= number:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": member.id}, update={"$set": {"money": e['money'] - number, "bank": e['bank']}})
            await ctx.send(f"You took {MONEY_EMOJI} {number} from {member.name}")
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": a['money'] + number, "bank": a['bank']}})

        elif e is None:
            ctx.command.reset_cooldown(ctx)
            embed = discord.Embed(title="Rob", description=f"{member.name} has no money to take", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            ctx.command.reset_cooldown(ctx)
            await ctx.send(f"{member.name} does not have much money so lets leave them")

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.member)
    async def beg(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            responses = ["Mr.Cat", "Nirlep", "Awoosh", "Avi", "Blue.", "Your Son"]
            response = random.choice(responses)
            number = random.randint(1, 15)
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Beg", description=f"{response} has gave you {MONEY_EMOJI} {number}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        else:
            responses = ["Mr.Cat", "Nirlep", "Awoosh", "Avi", "Blue.", "Your Son"]
            names = random.choice(responses)
            money_number = random.randint(1, 15)
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + money_number}})
            embed = discord.Embed(title="Beg", description=f"{names} has gave you {MONEY_EMOJI} {money_number}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": member.id})

        if e is None:
            embed = discord.Embed(title=f"Balance For {member.name}", description=f"{member.name} has No money", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"Balance For {member.name}", description=f"Wallet: {MONEY_EMOJI} {e['money']}\nBank: {MONEY_EMOJI} {e['bank']}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx: commands.Context):
        guild_lb = db.collection.find({"guild_id": ctx.guild.id}).limit(10)
        global_lb = db.collection.find({}).limit(10)

        guild_embed = discord.Embed(
            title="Guild Leaderboard",
            description="\n".join([f"**{self.bot.get_user(data['_user'])}** - `{data['money']}`" for data in guild_lb]),
            color=MAIN_COLOR
        )
        global_embed = discord.Embed(
            title="Global Leaderboard",
            description="\n".join([f"**{self.bot.get_user(data['_user'])}** - `{data['money']}`" for data in global_lb]),
            color=MAIN_COLOR
        )
        view = LeaderboardView(ctx, guild_embed, global_embed)
        await ctx.send(embed=guild_embed, view=view)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.member)
    async def daily(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": 100, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Daily", description=f"You got {MONEY_EMOJI} 100 from your daily", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        else:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + 100}})
            embed = discord.Embed(title="Daily", description=f"You got {MONEY_EMOJI} 100 from your daily", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command(help="Buy an item from the shop!")
    async def buy(self, ctx: commands.Context, item: ItemConverter = None, amount: Optional[int] = 1):
        if not item:
            return await ctx.reply("Please specify an item to buy!")
        if amount <= 0:
            return await ctx.reply("Please enter a positive value next time!")
        item: Item = item  # am just type hinting

        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            db.collection.insert_one({"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": 0, "bank": 0})
            raise NoMoney(0, item.prize * amount)
        if e['money'] < item.prize * amount:
            raise NoMoney(e['money'], item.prize * amount)

        items = e.get('items', {})
        if item.name in items:
            items[item.name] += amount
        else:
            items[item.name] = amount
        db.collection.update_one(
            filter={"guild_id": ctx.guild.id, "_user": ctx.author.id},
            update={"$set": {
                "money": e['money'] - item.prize * amount,
                "items": items
            }}
        )
        embed = discord.Embed(
            title="Item(s) Bought!",
            description=f"You bought {item.name} {amount} time(s) for {MONEY_EMOJI} {item.prize * amount}",
            color=MAIN_COLOR
        )
        await ctx.reply(embed=embed)

    @commands.command(help="Check your inventory!", aliases=['inv', 'bag'])
    async def inventory(self, ctx: commands.Context, user: Optional[discord.Member] = None):
        user = user or ctx.author
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": user.id})
        if e is None:
            embed = discord.Embed(title="Inventory", description=f"{user.name} has no items", color=MAIN_COLOR)
            await ctx.send(embed=embed)
        else:
            items = e.get('items', {})
            if not items:
                embed = discord.Embed(title="Inventory", description=f"{user.name} has no items", color=MAIN_COLOR)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Inventory", description=f"{user.name}'s items", color=MAIN_COLOR)
                for item, amount in items.items():
                    item = await ItemConverter().convert(ctx, item)
                    embed.add_field(name=f"{item.emoji} {item.name.title()}", value=amount, inline=False)
                await ctx.send(embed=embed)

    @has_item("fishing-rod")
    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.member)
    async def fish(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            number = random.randint(15, 250)
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Fishing", description=f"You made {MONEY_EMOJI} {number} from fishing", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        else:
            number = random.randint(15, 250)
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + number, "bank": e['bank']}})
            embed = discord.Embed(title="Fishing", description=f"You made {MONEY_EMOJI} {number} from fishing", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @has_item("shovel")
    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.member)
    async def dig(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            number = random.randint(15, 300)
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Dig", description=f"You made {MONEY_EMOJI} {number} from digging", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e['bank'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        else:
            number = random.randint(15, 300)
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + number, "bank": e['bank']}})
            embed = discord.Embed(title="Dig", description=f"You made {MONEY_EMOJI} {number} from digging", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.member)
    async def search(self, ctx):
        embed = discord.Embed(title="Search", description=f"You can search one of the 3 options for money (You can make up to {MONEY_EMOJI} 1000)", color=MAIN_COLOR)
        await ctx.send(embed=embed, view=Search(ctx))

    @commands.command()
    async def give(self, ctx, member: discord.Member, money_stuff: Union[int, str]):
        a = db.collection.find_one({"guild_id": ctx.guild.id, "_user": member.id})

        if a['bank'] is None:
            await ctx.send("This user has no bank")

        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e['money'] >= money_stuff:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": member.id}, update={"$set": {"money": a['money'] + money_stuff, "bank": a['bank']}})
            embed = discord.Embed(title="Given", description=f"You gave {MONEY_EMOJI} {money_stuff} to {member.name}", color=MAIN_COLOR)
            await ctx.send(embed=embed)
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] - money_stuff}})

        elif e['money'] is None:
            await ctx.send(f"Please run `{ctx.clean_prefix}work`")

        elif e is None:
            ctx.send("No money lol")

        else:
            await ctx.send("You don't have enough money")


def setup(bot):
    bot.add_cog(money(bot=bot))
