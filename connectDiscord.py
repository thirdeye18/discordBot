#!/usr/bin/env python3

"""
Discord Bot Handling Script
Author: Justin Hammel
Description: Script for connecting and handling the interaction of the bot with the
                server. Script expects there to be a Token for your bot and the name
                of your server placed into a file called .env in the same directory
                as all the other files for the script.
"""

"""External library imports"""

## importing discord api, enables interaction with discord
import discord
## import for handling .env files, .env files store credentials
from dotenv import load_dotenv
## Needed to access the .env files
import os
## allows random choices for the magic 8 ball feature
import random

load_dotenv()   # loading dotenv to handle .env files
## Discord token read into program from an environment variable for security
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

"""
Classes bundle data and functionality together. This allows creation of a new
object that can then have it's own methods.
MyClient is the new object that interacts with Discord through the API by
new methods with <async def>.
"""
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

        ## words for the bot to respond to as being not allowed in the server
        bad_words = ['cheat', 'cheats', 'hack', 'hacks', 'internal', 'external', 'ddos', 'denial of service']

        messageContent = message.content    # store the message in a string
        ## loop through the message looking for the key words
        if len(messageContent) > 0:     # make sure the message contains something
            for word in bad_words:
                if word in messageContent:
                    await message.delete()  # delete the message if it has key words
                    await message.channel.send('Do not say that!')

        ## There can als be keyword commands for the bot to respond to, begin with either !, or ? to prevent confusion
        if message.content.startswith('!hello'):
            await message.channel.send('Ello!', mention_author=True)
        if message.content.endswith("hello?"):
            await message.reply("No, I said ello, but that's close enough.")
        if message.content.endswith('?magic8ball'):     #need to make sure the question ends with key word to trigger
            magicResponse = random.choice(['It is certain','As i see it, yes', 'Dont count on it', 'Without a doubt', 'Definitely', 'Very doubtful', 'Outlook not so good', 'My sources say no', 'My reply is no', 'Most likely', 'You may rely on it', 'Ask again later'])
            await message.channel.send(magicResponse)
        ## command to disconnect bot on !quit
        # if message.content.startswith('quit'):


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

#bot = commands.Bot(command_prefix='?', description=description, intents=intents)
client = MyClient(intents = intents)
#bot.run(TOKEN)
client.run(TOKEN)
