from click import edit
import discord
from discord.ext import commands
from utils.database import db1 as db

class StarBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
       if payload.emoji.name == "⭐":
        if db.exists(f"starboard"):
            pass
        else:
            db.list_create("starboard")
            pass
        if (payload.emoji.name == "⭐") and (payload.message_id in db.list_get("starboard")):
            ### edit message
            db.update(f"message_star:{payload.message_id}", db.get(f"message_star:{payload.message_id}") + 1)
            edit_message_id = db.get(f"message:{payload.message_id}")
            edit_message_channel = db.get(f"message_channel:{payload.message_id}")
            edit_message = await self.bot.get_channel(edit_message_channel).fetch_message(edit_message_id)
            star_count = db.get(f"message_star:{payload.message_id}")
            content = db.get(f"message_content:{payload.message_id}")
            embed = discord.Embed(title=f"{payload.message_id}", description=f"{content}", color=0x00ff00,
            url=f"https://discordapp.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}")
            embed.set_footer(text=f"{star_count} | ⭐")
            await edit_message.edit(content=f"new star", embed=embed)
        else:
            db.list_add("starboard", payload.message_id)
            if (db.get(f"starboard_channel:{payload.guild_id}") is False):
                print("Starboard channel not set")
            else:
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                channel_id = db.get(f"starboard_channel:{payload.guild_id}")
                channel = self.bot.get_channel(channel_id)
                embed = discord.Embed(title=f"{payload.message_id}", description=f"{msg.content}", color=0x00ff00, 
                url=f"https://discordapp.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id}")
                embed.set_footer(text=f"1 | ⭐")
                msg_id = await channel.send(embed=embed)
                db.set(f"message_star:{payload.message_id}", 1)
                db.set(f"message:{payload.message_id}", msg_id.id)
                db.set(f"message_content:{payload.message_id}", msg.content)
                db.set(f"message_channel:{payload.message_id}", msg.channel.id)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        msg_star_count = 0
        for e in msg.reactions:
                 if e.emoji == '⭐':
                  msg_star_count += e.count
                  break
        if (payload.emoji.name == "⭐") and (payload.message_id in db.list_get("starboard")) and (msg_star_count == 0):
            message_id = db.get(f"message:{payload.message_id}")
            message_channel = db.get(f"message_channel:{payload.message_id}")
            msg = await self.bot.get_channel(message_channel).fetch_message(message_id)
            await msg.delete()
            db.list_delete("starboard", payload.message_id)
            db.delete(f"message:{payload.message_id}")
            db.delete(f"message_content:{payload.message_id}")
            db.delete(f"message_channel:{payload.message_id}")
            db.delete(f"message_star:{payload.message_id}")
        else:
            pass

    @commands.Cog.listener(name="on_message_delete")
    async def starboard_message_delete(self, message):
        if db.exists(f"message:{message.id}"):
            message_id = db.get(f"message:{message.id}")
            message_channel = db.get(f"message_channel:{message.id}")
            msg = await self.bot.get_channel(message_channel).fetch_message(message_id)
            await msg.delete()
            db.delete(f"message:{message.id}")
            db.delete(f"message_content:{message.id}")
            db.delete(f"message_channel:{message.id}")
            db.delete(f"message_star:{message.id}")
        else:
            pass

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def starboard(self, ctx, channel: discord.TextChannel):
        if db.exists(f"starboard_channel:{ctx.guild.id}"):
            db.update(f"starboard_channel:{ctx.guild.id}", channel.id)
            await ctx.send(f"Starboard channel set to {channel.mention}")
        else:
            db.set(f"starboard_channel:{ctx.guild.id}", channel.id)
            await ctx.send(f"Starboard channel set to {channel.mention}")

async def setup(bot):
    await bot.add_cog(StarBoard(bot))