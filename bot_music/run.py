import os
import discord

from discord.ext import commands

from bot.music_bot import MusicBot
from bot.text_bot import TextBot


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    description='gachiBASS Clap'
)
bot.add_cog(MusicBot(bot))
bot.add_cog(TextBot(bot))


@bot.event
async def on_ready():
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))

bot.run(os.environ['GACHIBOT_TOKEN'])

