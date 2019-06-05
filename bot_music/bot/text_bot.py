import textwrap
import datetime
import os
from discord.ext import commands
from .github import Github
from discord.utils import get


class TextBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """ Emoji reacts to someone who says 'pubg' """
        if ctx.author == self.bot.user:
            return
            
        if 'pubg' in ctx.content.lower() or 'pupk' in ctx.content.lower() or 'пубг' in ctx.content.lower() or 'пабг' in ctx.content.lower() or 'пупк' in ctx.content.lower():
            await ctx.add_reaction(get(self.bot.emojis, name='gav'))
            await self.bot.process_commands(ctx)
    

    @commands.command()
    async def zaebat(self, ctx):
        """ Zaebat' Deman'a """

        sosna = ctx.guild.get_member(268702321662230539)
        await ctx.send('И охуенен 👉 {}'.format(sosna.mention))

    @commands.command()
    async def pubg(self, ctx):
        """ Let's play some pubg """
        pass

    @commands.command()
    async def pupk(self, ctx):
        """ !pubg alias """
        pass

    @commands.command()
    async def restart(self, ctx):
        await ctx.send('I\'ll be back!' )
        os.system('DELETE \/apps\/gachi-bot-app\/dynos') 

    @pubg.before_invoke
    @pupk.before_invoke
    async def __pubg(self, ctx):
        await ctx.send('{0} {0} {0}'.format(get(self.bot.emojis, name='gav')))

