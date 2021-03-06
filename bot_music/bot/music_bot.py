import discord
import json
import random
import asyncio

from discord.ext import commands
from discord.utils import get
from .ytdl import YTDLSource
from collections import deque
from .user import User


class MusicBot(commands.Cog, User):

    

    id_channel = 570419462453592076	#release
    #id_channel = 570646876207054859		#test

    def __init__(self, bot):

        self.debug_log = False

        self.bot = bot
        self.volume_lvl = 0.5
        self.owner_last_id = None
        self.owner_last_channel = None
        self.Users = []

        self.autoplay = 0 #autoplay next track yt

        with open('song_list.json') as json_data:
            self.gachi_list = json.load(json_data)

    @commands.command()
    async def comeon(self, ctx, *, channel: discord.VoiceChannel=None):
        """ Joins a voice channel """

        if self.get_owner_id() is None or self.get_owner_id() == ctx.author.id:
            if ctx.channel.id == MusicBot.id_channel:
                if channel is None and ctx.author.voice is None:
                    return await ctx.send("You are not connected to a voice channel.")

                channel = channel or ctx.author.voice.channel
                if ctx.voice_client:
                    await ctx.voice_client.move_to(channel)
                else:
                    await channel.connect()   

                self.set_owner(ctx.author.id)
                self.owner_last_channel = self.get_owner_channel()
                self.owner_last_id = self.get_owner_id()

                self.debuglog("comeon func")

                await asyncio.sleep(15)    
                if ctx.voice_client and ctx.voice_client.is_playing() == False:                    
                    if self.get_owner_id():
                        await ctx.voice_client.disconnect()
                        self.clr_owner()
                        self.owner_last_channel = None
                        self.owner_last_id = None
        else:
            await MusicBot.__isNotOwner(self, ctx)

        


    @commands.command()
    async def gachi(self, ctx):
        """ Plays a song from the gachi list """

        if self.__isOwner(ctx):
            song = random.choice(self.gachi_list)
            url = 'https://www.youtube.com/watch?v={}'.format(song['url'])
            await self.__yt(ctx, url)
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def yt(self, ctx, *, url):
        """ Play from the given url / search for a song """
        if self.get_owner_id() is None:
            self.set_owner(ctx.author.id)

        if ctx.author.id == self.get_owner_id():
            if ctx.author.voice is not None:
                if ctx.channel.id == MusicBot.id_channel:
                    await self.__yt(ctx, url)
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def pause(self, ctx):
        """ Pauses current track """

        if self.__isOwner(ctx, False):
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.pause()
        else:
            await MusicBot.__isNotOwner(self, ctx)

    @commands.command()
    async def resume(self, ctx):
        """ Resumes current track """

        if self.__isOwner(ctx, False):
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

        if self.__isOwner(ctx, False):
            await ctx.voice_client.disconnect()
            self.clr_owner()
        else:
            await MusicBot.__isNotOwner(self, ctx)
    '''
    @commands.command()
    async def forward(self, ctx, second: int):
    	if ctx.voice_client:
    		player = ctx.voice_client.source
    		print("playre: " +str(player))
    '''

    @gachi.before_invoke
    @yt.before_invoke
    async def __ensure_voice(self, ctx):

        channel = None

        if ctx.author.voice and ctx.author.voice.channel:   
            if not channel:
                try:
                    channel = ctx.author.voice.channel
                except AttributeError:
                    raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client
        if channel:
            if vc:
                if vc.channel.id == channel.id:
                    return
                try:
                    await vc.move_to(channel)
                except asyncio.TimeoutError:
                    raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
            else:
                try:
                    await channel.connect()
                except asyncio.TimeoutError:
                    raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        self.debuglog("Voice state has been changed.")
        self.upd_user_channel(member.id, after.channel)
        bot_channel = self.get_bot_channel(self.bot.user.id)

        if after.channel and (member.id == self.get_owner_id or member.id == self.owner_last_id):
            if member.voice.channel:
                if after.channel.id != self.owner_last_channel.id:
                    self.debuglog("owner leave channel")
                    self.clr_owner()
        
            self.debuglog("Get owner: " +str(self.get_owner_id()))

            if(self.get_owner_id() is None):
                if member.id == self.owner_last_id and after.channel.id == self.owner_last_channel.id and bot_channel and bot_channel.id == self.owner_last_channel.id: 
                    self.debuglog("Owner reconnect")
                    self.set_owner(member.id)
        elif member.id == self.get_owner_id():
            self.debuglog("owner disconnect voice")
            self.clr_owner()

        #if self.debug_log: self.print_users()

    @commands.Cog.listener()
    async def on_ready(self):
        members = self.bot.get_all_members()
        User.get_users(self,members)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        self.add_user(member)

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        self.remove_user(member.id)

    @yt.error
    async def yt_on_error(self, ctx, error):
        print('Error: ' + str(error))
        await ctx.send("error")

    async def __yt(self, ctx, url, silent=False):
        async with ctx.typing():        	
            player = await YTDLSource.from_url(
                url,
                loop=self.bot.loop,
                stream=False,
                volume=self.volume_lvl
            )
            ctx.voice_client.play(
                player,
                after=lambda e: print('Player error: %s' % e) if e else None
            )

        if not silent:

            self.owner_last_channel = self.get_owner_channel()
            self.owner_last_id = self.get_owner_id()

            await ctx.send(
                'Now playing: {0} [{1}]'.format(player.title, player.time)
            )   

            fulltime = float(player.time.total_seconds())
            delay = float(player.time.total_seconds() + 5.0)

            self.debuglog("delay time(full,delay): {0} , {1}".format(fulltime, delay))

            if delay > 305:
                delay = 305

            self.debuglog("To be sleep thread...")
            await asyncio.sleep(delay)

            print("unsleep")
            if self.__checkVoiceState(ctx):
                await ctx.voice_client.disconnect()
                self.clr_owner()
                return
            else:
                self.debuglog("owner is not None or owner not change")

            if(delay < fulltime):
                await asyncio.sleep(fulltime - delay)

            if self.__checkVoiceState(ctx):
                await ctx.voice_client.disconnect()
                self.clr_owner()
                self.owner_last_channel = None
                self.owner_last_id = None



    async def __isNotOwner(self, ctx):
        await ctx.send("You are not the owner of the running command.")


    def __isOwner(self, ctx, SetOwner: bool = True):
        if SetOwner:
            if self.get_owner_id() is None:
                self.set_owner(ctx.author.id)

        if ctx.author.id == self.get_owner_id():
            if ctx.channel.id == MusicBot.id_channel:
                return True
        return False

    def __checkVoiceState(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing() == False:
            return True
        else:
            return False        	

