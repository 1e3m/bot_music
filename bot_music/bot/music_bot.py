import discord
import json
import random
import asyncio

from discord.ext import commands
from discord.utils import get
from .ytdl import YTDLSource
from collections import deque

class Owner():
	def __init__(self, Id, Channel, Hash, State: bool):
		self.Id = Id
		self.Channel = Channel
		self.Hash = Hash
		self.State = State

	def __del__(self):
		print("clear session")

class MusicBot(commands.Cog):

	#id_channel = 570419462453592076	#release
    id_channel = 570646876207054859		#test

    def __init__(self, bot):
        self.bot = bot
        self.volume_lvl = 0.5

        self.owner = None
        self.owner_channel = None

        self.autoplay = 0 #autoplay next track yt
        self.owner_session = []

        with open('song_list.json') as json_data:
            self.gachi_list = json.load(json_data)

        MusicBot.create_session(self, bot)

    def create_session(self, bot):
    	print(self.bot.users)
    	for user in self.bot.get_all_members():
    		self.owner_session.append(Owner(user.id, user.channel.id, ranrom.random(), False))
    		print("Usr appended (Id: {0}), (chId: {1}), (rnd: {2}), (State: {3}) \n".format(user.Id, user.Channel, user.Hash, user.State))
    	print("Session appended")	

    def get_owner_session(self, Id):
    	for x in self.owner_session:
    		if x.Id == Id:
    			return x

    def set_owner_session(self,Id):
    	for x in self.owner_session:
    		if x.Id == Id:
    			x.State = True
    		else:
    			x.State = False

    def print_session(self):
    	print("-----------------------------SESSION TABLE-----------------------------------------")
    	for user in self.owner_session:
    		 print("User = (Id: {0}), (chId: {1}), (rnd: {2}), (State: {3}) \n".format(user.Id, user.Channel, user.Hash, user.State))
    	print("-----------------------------------------------------------------------------------")


    @commands.command()
    async def comeon(self, ctx, *, channel: discord.VoiceChannel=None):
        """ Joins a voice channel """
        #MusicBot.print_session(self)

        if self.owner is None:
            if ctx.channel.id == MusicBot.id_channel:
                if channel is None and ctx.author.voice is None:
                    return await ctx.send("You are not connected to a voice channel.")

                channel = channel or ctx.author.voice.channel
                if ctx.voice_client:
                    await ctx.voice_client.move_to(channel)
                else:
                    await channel.connect()

                #MusicBot.create_session(self, ctx.guild.users)
                #MusicBot.print_session(self)    

                self.owner = ctx.author.id

                #self.owner_session.append(Owner(ctx.author.id, ctx.author.voice.channel.id, random.random(), True))

                #print("user: " + MusicBot.get_owner_session(self, ctx.author.id))	
                #user = MusicBot.get_owner_session(self, ctx.author.id)

                #print("\n")
                #print(str(MusicBot.get_owner_session(self, ctx.author.id).Id))	
                #print("\n")
                #print("User = (Id: {0}), (chId: {1}), (rnd: {2}), (State: {3})".format(user.Id, user.Channel, user.Hash, user.State))	
                #print("\n")

                print("comeon func")
                print("owner: " +str(self.owner))
        else:
            await MusicBot.__isNotOwner(self, ctx)

    #old_version
    '''   
    @commands.command()
    async def comeon(self, ctx, *, channel: discord.VoiceChannel=None):
        """ Joins a voice channel """
        if self.owner is None:
            if ctx.channel.id == MusicBot.id_channel:
                if channel is None and ctx.author.voice is None:
                    return await ctx.send("You are not connected to a voice channel.")

                channel = channel or ctx.author.voice.channel
                if ctx.voice_client:
                    await ctx.voice_client.move_to(channel)
                else:
                    await channel.connect()

                self.owner = ctx.author.id

                self.owner_session.append(Owner(ctx.author.id, ctx.author.voice.channel.id, random.random(), True))

                #print("user: " + MusicBot.get_owner_session(self, ctx.author.id))	
                user = MusicBot.get_owner_session(self, ctx.author.id)

                print("\n")
                print(str(MusicBot.get_owner_session(self, ctx.author.id).Id))	
                print("\n")
                print("User = (Id: {0}), (chId: {1}), (rnd: {2}), (State: {3})".format(user.Id, user.Channel, user.Hash, user.State))	
                print("\n")

                print("session: " +self.owner_session[0])	
                print("comeon func")
                print("owner: " +str(self.owner))
        else:
            await MusicBot.__isNotOwner(self, ctx)
    '''

    @commands.command()
    async def gachi(self, ctx):
        """ Plays a song from the gachi list """
        if self.owner is None:
            self.owner = ctx.author.id

        if ctx.author.id == self.owner:
            if ctx.channel.id == MusicBot.id_channel:
                song = random.choice(self.gachi_list)
                url = 'https://www.youtube.com/watch?v={}'.format(song['url'])
                await self.__yt(ctx, url)
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def yt(self, ctx, *, url):
        """ Play from the given url / search for a song """
        if self.owner is None:
            self.owner = ctx.author.id

        if ctx.author.id == self.owner:
            if ctx.author.voice is not None:
                if ctx.channel.id == MusicBot.id_channel:
                    await self.__yt(ctx, url)
                    print("yt owner: " +str(self.owner))
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def pause(self, ctx):
        """ Pauses current track """
        if ctx.author.id == self.owner:
            if ctx.channel.id == MusicBot.id_channel:
                if ctx.voice_client and ctx.voice_client.is_playing():
                    ctx.voice_client.pause()
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def resume(self, ctx):
        """ Resumes current track """
        if ctx.author.id == self.owner:
            if ctx.channel.id == MusicBot.id_channel:
                if ctx.voice_client and ctx.voice_client.is_paused():
                    ctx.voice_client.resume()
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume """
        if ctx.channel.id == MusicBot.id_channel:        

            if ctx.voice_client is None:
                return await ctx.send("Not connected to a voice channel.")

            self.volume_lvl = volume / 100
            ctx.voice_client.source.volume = self.volume_lvl
            await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def fuckyou(self, ctx):
        """ Stops and disconnects the bot from voice """
        if ctx.author.id == self.owner:
            if ctx.channel.id == MusicBot.id_channel:
                sosna = ctx.guild.get_member(188000465550573569)
                if ctx.author == sosna:
                    return await ctx.send('Oh, fuck you leather man')

                await ctx.voice_client.disconnect()
            self.owner = None
            print("owner: " +str(self.owner))
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def forward(self, ctx, second: int):
    	if ctx.voice_client:
    		player = ctx.voice_client.source
    		print("playre: " +str(player))

    @gachi.before_invoke
    @yt.before_invoke
    async def __ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
    	if(self.owner is not None):
    		if member.id == self.owner and after.channel.id != self.owner_channel:
    			self.owner = None 

    async def __yt(self, ctx, url, silent=False):
        async with ctx.typing():        	
            player = await YTDLSource.from_url(
                url,
                loop=self.bot.loop,
                stream=True,
                volume=self.volume_lvl
            )
            ctx.voice_client.play(
                player,
                after=lambda e: print('Player error: %s' % e) if e else None
            )

        if not silent:

            last_owner = self.owner
            self.owner_channel = ctx.author.voice.channel.id

            await ctx.send(
                'Now playing: {0} [{1}]'.format(player.title, player.time)
            )   

            fulltime = float(player.time.total_seconds())
            delay = float(player.time.total_seconds() + 5.0)

            print("time(full,delay): {0} , {1}".format(fulltime, delay))

            if delay > 305:
                delay = 305

            await asyncio.sleep(delay)
            print("unsleep")
            if last_owner == self.owner and (ctx.author.voice is None or self.owner_channel != ctx.author.voice.channel.id):
                await ctx.voice_client.disconnect()
                self.owner = None
                return
            else:
                print("owner is not None or owner not change")

            await asyncio.sleep(fulltime - delay)
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
                self.owner = None



    async def __isNotOwner(self, ctx):
        await ctx.send("You are not the owner of the running command.")

