#!/usr/bin/env python3

"""
Discord Bot Handling Script
Author: Justin Hammel
Description: Script for connecting and handling the interaction of the bot with the
                server. Script expects there to be a Token for your bot and the name
                of your server placed into a file called .env in the same directory
                as all the other files for the script.
"""

## External library imports
## os enables miscellaneous operating system interfaces(don't think this is needed here?)
import os
## importing discord api, enables interaction with discord
import discord
from discord.ext import commands    # for running commands easier than using @client.event
## import for handling .env files, .env files store credentials
from dotenv import load_dotenv
## allows random choices for the magic 8 ball feature
import random

load_dotenv()
## Discord token read into program from an environment variable for security
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = '''An example bot to showcase the discord.ext.commands extension module. There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

## client represents connection to discord, similar to a sftp object
## handles events, tracks state, and interacts with Discord APIs
class MyClient(discord.Client):
    async def on_ready(self):
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        print(f'{client.user} has connected to the following server:')  # print the bots name
        print(f'{guild.name}(id: {guild.id})')  # print the server name and id
        ## Print out the members of the server
        members = '\n - '.join([member.name for member in guild.members])   # Puts all the guild members names in a list
        print(f'Guild Members:\n - {members}')

    async def on_message(self, message):
        ## First if loop checks to see if the message came from the bot prevents recursive calls
        if message.author == self.user:
            return
        if message.content.startswith('!hello'):
            await message.channel.send('Hello World!', mention_author=True)
        if message.content.startswith('?magic8ball'):
            magicResponse = random.choice(['It is certain','As i see it, yes', 'Dont count on it', 'Without a doubt', 'Definitely', 'Very doubtful', 'Outlook not so good', 'My sources say no', 'My reply is no', 'Most likely', 'You may rely on it', 'Ask again later'])
            await message.channel.send(magicResponse)

    ## Greeting when new member joins the chat
#    async def on_member_join(self, member):
#        guild = member.guild
#        if guild.system_channel is not None:
#            await guild.system_channel.send(f'Ello {0.mention}, fancy a cuppa?'.format(member, guild))
#            await member.create_dm()    # Next part will send a DM to the member that just joined the channel
#            await member.dm_channel.send(f'Ello {member.name}, lovely server innit!')

#        if message.content == 'hello':
#            response = "No, I said ello, but that's close enough"
#            await message.channel.send(response)

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot.run(TOKEN)
client = MyClient(intents = intents)
client.run(TOKEN)
