import logging

import discord
from discord.ext import commands

from config import MAIN_COLOR
import aiohttp
import io


class images(commands.Cog, description="This is where you can get images"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Images is ready')

    @commands.command()
    async def horny(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.replace(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                        title="bonk",
                        color=MAIN_COLOR,
                    )
                    em.set_image(url="attachment://horny.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No horny :(')
        await session.close()

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
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
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No gay :(')
        await session.close()

    @commands.command()
    async def jail(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.replace(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "jail.png")
                    em = discord.Embed(
                        title="He be in jail",
                        color=MAIN_COLOR,
                    )
                    em.set_image(url="attachment://jail.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No jial :(')
        await session.close()

    @commands.command()
    async def gun(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.monkedev.com/canvas/gun?imgUrl={member.avatar.replace(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gun.png")
                    em = discord.Embed(
                        title="Get down he has a gun",
                        color=MAIN_COLOR,
                    )
                    em.set_image(url="attachment://gun.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No gun :(')
        await session.close()

    @commands.command()
    async def comment(self, ctx, *, text=None):
        if text is None:
            await ctx.send("You need to add text to this")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar.url}&username={ctx.author.name}&comment={text}') as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "comment.png")
                        em = discord.Embed(
                            title="Comment",
                            color=MAIN_COLOR,
                        )
                        em.set_image(url="attachment://comment.png")
                        await ctx.send(embed=em, file=file)

    @commands.command()
    async def message(self, ctx, member: discord.Member = None, *, text=None):
        member = member or ctx.author
        if text is None:
            await ctx.send("You need to add text to this")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.monkedev.com/canvas/fakequote?imgUrl={member.avatar.url}&text={text}&username={member.name}') as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "comment.png")
                        em = discord.Embed(
                            title="Comment",
                            color=MAIN_COLOR,
                        )
                        em.set_image(url="attachment://comment.png")
                        await ctx.send(embed=em, file=file)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member = None):
            member = member or ctx.author
            embed = discord.Embed(title=f"Avatar of {member.name}", color=MAIN_COLOR)
            embed.set_image(url=member.avatar.url)
            await ctx.send(embed=embed)

    @commands.command()
    async def pikachu(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/pikachu')
            json = await request.json()
            embed = discord.Embed(title="Pika Pika!", color=MAIN_COLOR)
            embed.set_image(url=json['link'])
            await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/dog')
            json = await request.json()
            embed = discord.Embed(title="Woof Woof!", color=MAIN_COLOR)
            embed.set_image(url=json['link'])
            await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/cat')
            json = await request.json()
            embed = discord.Embed(title="Meow!", color=MAIN_COLOR)
            embed.set_image(url=json['link'])
            await ctx.send(embed=embed)

    @commands.command()
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/img/panda')
            json = await request.json()
            embed = discord.Embed(title="Panda!", color=MAIN_COLOR)
            embed.set_image(url=json['link'])
            await ctx.send(embed=embed)
            
    @commands.command(description='You can kiss your friend or lover')
    async def kiss(self, ctx, member: discord.Member):

      if member == ctx.author:
       embed1 = discord.Embed(title="Oh no", description=f"Kiss! {self.bot.user.name} kissed {member.display_name}", color=MAIN_COLOR)
       await ctx.send(embed=embed1)
       return

      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/kiss')
       json = await request.json()
       embed = discord.Embed(title=f"Awww! {ctx.author.name} kissed {member.display_name}", color=MAIN_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='You can slap your friend or lover')
    async def slap(self, ctx, member: discord.Member):

      if member == ctx.author:
       embed1 = discord.Embed(title="Oh no", description=f"NO! lets not do that", color=MAIN_COLOR)
       await ctx.send(embed=embed1)
       return
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/slap')
       json = await request.json()
       embed = discord.Embed(title=f"HEYY! {ctx.author.name} slaped {member.display_name}", color=MAIN_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='You can poke your friend or lover')
    async def poke(self, ctx, member: discord.Member):

      if member == ctx.author:
       embed1 = discord.Embed(title="Oh no", description=f"Poke! {self.bot.user.name} poked {member.display_name}", color=MAIN_COLOR)
       await ctx.send(embed=embed1)
       return

      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/poke')
       json = await request.json()
       embed = discord.Embed(title=f"Poke! {ctx.author.name} poked {member.display_name}", color=MAIN_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='You can tickle your friend or lover')
    async def tickle(self, ctx, member: discord.Member):

      if member == ctx.author:
       embed1 = discord.Embed(title="Oh no", description=f"Tickle! {self.bot.user.name} tickled {member.display_name}", color=MAIN_COLOR)
       await ctx.send(embed=embed1)
       return

      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/tickle')
       json = await request.json()
       embed = discord.Embed(title=f"Tickle! {ctx.author.name} tickled {member.display_name}", color=MAIN_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='You can hug your friend or lover')
    async def hug(self, ctx, member: discord.Member):

      if member == ctx.author:
       embed1 = discord.Embed(title="Oh no", description=f"Hug! {self.bot.user.name} huged {member.display_name}", color=MAIN_COLOR)
       await ctx.send(embed=embed1)
       return

      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/hug')
       json = await request.json()
       embed = discord.Embed(title=f"Huggies! {ctx.author.name} huged {member.display_name}", color=MAIN_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='You can cuddle your friend or lover')
    async def cuddle(self, ctx, member: discord.Member):

      if member == ctx.author:
       embed1 = discord.Embed(title="Oh no", description=f"Cuddle! {self.bot.user.name} cuddled {member.display_name}", color=MAIN_COLOR)
       await ctx.send(embed=embed1)
       return

      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/cuddle')
       json = await request.json()
       embed = discord.Embed(title=f"Cuddles! {ctx.author.name} cuddled {member.display_name}", color=MAIN_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='Cry when you need to')
    async def cry(self, ctx):
        async with aiohttp.ClientSession() as session:
         request = await session.get('https://purrbot.site/api/img/sfw/cry/gif')
         json = await request.json()
         embed = discord.Embed(title="They need a hug", color=MAIN_COLOR)
         embed.set_image(url=json['link'])
         await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(images(bot=bot))
