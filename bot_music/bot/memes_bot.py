import discord
import asyncio
import json
import aiohttp


from requests_html import AsyncHTMLSession
from discord.ext import commands



class MemesBot(commands.Cog):

    mem_text_channel = None

    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://admem.ru/rndm'
        self.joke_url = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'
        self.asession = AsyncHTMLSession()

    @commands.Cog.listener()
    async def on_ready(self):
        
        channels = self.bot.get_all_channels()
        Category = None

        for cat in channels:
            if(cat.name == 'Текстовые каналы'):
                Category = cat
       
        channels = self.bot.get_all_channels()

        for ch in channels:
            if(ch.name == 'мемы'):
                MemesBot.mem_text_channel = ch.id
                return


        if(MemesBot.mem_text_channel is None):
            Guilds = self.bot.guilds 
            for guild in Guilds:    
                channel = await guild.create_text_channel('мемы',category=Category)
                MemesBot.mem_text_channel = channel.id
                return

            

    @commands.command()
    async def meme(self, ctx):
        """ Send meme on channel """        
        if ctx.channel.id == MemesBot.mem_text_channel:  

            async def get_code():
                r = await self.asession.get(self.url)
                await r.html.arender(sleep=1, keep_page=True)
                return r

            response = await get_code() 
            noindex = response.html.find('noindex', first=True)
            img = noindex.xpath('//img')[0]

            await ctx.send('http:' + img.attrs['src'])

    @commands.command()
    async def joke(self,ctx):
        """ Send joke on channel """  
        async with aiohttp.ClientSession() as sess:
            async with sess.get(self.joke_url) as resp:

                text = (await resp.text()).replace('\r\n', '\\r\\n')

                data = json.loads(text)
                joke = data['content']

        await ctx.send( '```' + str(joke) + '```')

