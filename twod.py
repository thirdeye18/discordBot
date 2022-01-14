#!/usr/bin/env python3

import discord  # discord api
from discord.ext import commands  # easier bot commands
import youtube_dl  # download YouTube audio for music in voice chat
import asyncio  # for async calls
from dotenv import load_dotenv  # to handle .env file
import os  # to access the filesystem for the .env files
from chatbot import chatbot  # chatbot imported from script
import asyncio_runtime_error_event_loop_closed_fix

# import random   # for random functions (dice, 8ball)
# from dieRoller import * # example dice function

"""
Discord Bot Handling Script
Author: Justin Hammel
Description: Script for connecting and handling the interaction of the bot with the
            server. Script expects there to be a Token for your bot and the name
            of your server placed into a file called .env in the same directory
            as all the other files for the script.
"""

# Retrieve data from .env file
load_dotenv()  # loading dotenv to handle .env files
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents().all()
client = discord.Client(intents=intents)
# create bot instance, set prefix for chat commands
bot = commands.Bot(command_prefix='!', intents=intents, description='Your friendly neighborhood AI')

"""
Setup options for youtube_dl and FFMPEG conversion
"""
youtube_dl.utils.bug_reports_message = lambda: ''  # Suppress noise about console usage from errors
# Options for music being played
ytdl_format_options = {
    'format': 'bestaudio/best',
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
# ffmpeg video conversion options, -vn strips video from files being played, leaves just audio
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

"""
Handles download and conversion of YouTube. Finds and downloads first video from search results. Search is passed in 
from the !play command. Videos are converted to audio only format with ffmpeg.
"""


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return filename


"""
Specific youtube music bot commands
"""


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:  # only allows ppl in chanel to give commands
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='play_song', help='To play song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

""" 
Print message when the bot is ready and online 
"""


@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "general":
                await channel.send('Bot Activated..')
                await channel.send(file=discord.File(r'F:\01-coding\discordBot\2d.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))
    print('------')


""" 
Bot commands not related to playing music/voice chat functions 
"""


@bot.command(name='hello', help='Bot says Ello')
async def hello(ctx):
    await ctx.send("Ello!")


@bot.command(name='log_out', help='make bot leave channel')
async def log_out(ctx):
    await ctx.send("TTFN!")
    await bot.close()


"""
chatbot commands below here
"""


@bot.command(name='2d', help='Bot responds to Hello with AI')
async def chatter_response(ctx):
    await ctx.send(chatbot.get_response("Hello 2d"))


@bot.command(name='2dtalk', help='Send personalized text to bot')
async def custom_chatter(ctx, arg):
    print(arg)
    await ctx.send(chatbot.get_response(arg))
