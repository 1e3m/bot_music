import textwrap
import datetime
from discord.ext import commands
from .github import Github
from discord.utils import get


class TextBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    '''
    @commands.event
    async def on_message(self, ctx):
        """ Emoji reacts to someone who says 'pubg' """
        print('gav')
        if ctx.author == self.bot.user:
            return
        if 'pubg' in ctx.content.lower() or 'pupk' in ctx.content.lower() or 'пубг' in ctx.content.lower() or 'пабг' in ctx.content.lower() or 'пупк' in ctx.content.lower():
            gav = get(self.bot.emojis, name='gav')
            await ctx.add_reaction(gav)
            await self.bot.process_commands(ctx)
    '''
    @pubg.before_invoke
    @pupk.before_invoke
    async def __pubg(self, ctx):
        await ctx.send('{0} {0} {0}'.format(get(self.bot.emojis, name='gav')))
        #emogiList = self.bot.emojis
        #for item in emogiList:
        #    if item.name == 'gav':
        #        gav = self.bot.get_emoji(item.id)
        #        await ctx.send('{0} {0} {0}'.format(gav))
