#!/usr/bin/env python3
"""
Discord Bot Handling Script
Author: Justin Hammel
Description: Script for connecting and handling the interaction of the bot with the
            server. Script expects there to be a Token for your bot and the name
            of your server placed into a file called .env in the same directory
            as all the other files for the script.
"""

"""
External library imports
"""
import discord  # discord api
from discord.ext import commands, tasks  # easier bot commands
import youtube_dl  # download YouTube audio for music in voice chat
import asyncio
from dotenv import load_dotenv  # to handle .env file
import os  # to access the filesystem for the .env files

# import random   # for random functions (dice, 8ball)
# from dieRoller import * # example dice function

"""
Here's where we pull the token from the .env file for security reasons
"""
load_dotenv()  # loading dotenv to handle .env files
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

"""
This is the youtube magic and setup options for youtube_dl
"""
youtube_dl.utils.bug_reports_message = lambda: ''  # Suppress noise about console usage from errors

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


"""
Specific youtube music bot commands
"""


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


intents = discord.Intents().all()  # intents are permissions for the bot
bot = commands.Bot(command_prefix='!', description='Relatively simple music bot example')

""" Print message when the bot is ready and online """


@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "general":
                await channel.send('Bot Activated..')
                await channel.send(file=discord.File(r'C:\Users\Justin\github\discordBot\2d.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))
    print('------')


""" Bot commands """


@bot.command(name='hello', help='Bot says Ello')
async def hello(ctx):
    await ctx.send("Ello!")


## These have now been moved specifically to
# @bot.command(name='join', help='Tells the bot to join the voice channel')
# async def join(ctx):
#     if not ctx.message.author.voice:
#         await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
#         return
#     else:
#         channel = ctx.message.author.voice.channel
#         await channel.connect()
#
# @bot.command(name='leave', help='To make the bot leave the voice channel')
# async def leave(ctx):
#     voice_client = ctx.message.guild.voice_client
#     if voice_client.is_connected():
#         await voice_client.disconnect()
#     else:
#         await ctx.send("The bot is not connected to a voice channel.")
#
# @bot.command(name='play_song', help='To play song')
# async def play(ctx,url):
#     try :
#         server = ctx.message.guild
#         voice_channel = server.voice_client
#
#         async with ctx.typing():
#             filename = await YTDLSource.from_url(url, loop=bot.loop)
#             voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
#         await ctx.send('**Now playing:** {}'.format(filename))
#     except:
#         await ctx.send("The bot is not connected to a voice channel.")
#
#
# @bot.command(name='pause', help='This command pauses the song')
# async def pause(ctx):
#     voice_client = ctx.message.guild.voice_client
#     if voice_client.is_playing():
#         await voice_client.pause()
#     else:
#         await ctx.send("The bot is not playing anything at the moment.")
#
# @bot.command(name='resume', help='Resumes the song')
# async def resume(ctx):
#     voice_client = ctx.message.guild.voice_client
#     if voice_client.is_paused():
#         await voice_client.resume()
#     else:
#         await ctx.send("The bot was not playing anything before this. Use play_song command")
#
# @bot.command(name='stop', help='Stops the song')
# async def stop(ctx):
#     voice_client = ctx.message.guild.voice_client
#     if voice_client.is_playing():
#         await voice_client.stop()
#     else:
#         await ctx.send("The bot is not playing anything at the moment.")

bot.add_cog(Music(bot))
bot.run(TOKEN)
