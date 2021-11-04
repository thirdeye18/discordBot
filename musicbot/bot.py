"""
Discord Bot Handling Script
Description: Script for connecting and handling the interaction of the bot with the
            server. Script expects there to be a Token for your bot and the name
            of your server placed into a file called .env in the same directory
            as all the other files for the script.
"""

"""
External library imports
"""
import discord  # discord api
from discord.ext import commands    # easier bot commands
from . import config
from .cogs import music, error, meta, tips

cfg = config.load_config()  # Loading config file

intents = discord.Intents().all()   # intents are permissions for the bot
bot = commands.Bot(command_prefix=cfg["prefix"])

""" Print message when the bot is ready and online """
@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await channel.send('Bot Activated..')
                await channel.send(file=discord.File(r'C:\Users\Justin\github\discordBot\2d.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))
    print('------')

COGS = [music.Music, error.CommandErrorHandler, meta.Meta, tips.Tips]
