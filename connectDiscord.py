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
# importing discord api, enables interaction with discord
# Second import is for bot command abstraction (easy commands)
import discord
# from discord.ext import commands,tasks
# For future music functionality
import youtube_dl
# import for handling .env files, .env files store credentials
from dotenv import load_dotenv
# Needed to access the .env files
import os
# allows random choices for the magic 8 ball feature
import random
# import my dice rolling function
from dieRoller import *

load_dotenv()  # loading dotenv to handle .env files
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
        ## Printing the bots name to the console
        print(f"{client.user} has connected to the following server:")
        print(f"{guild.name}(id: {guild.id})")  # print the server name and id
        ## Print out the members of the server in the console
        ## First part puts all the member's names in a list
        members = '\n - '.join([member.name for member in guild.members])
        print(f"Guild Members:\n - {members}")

    async def on_message(self, message):
        ## checks if the message came from the bot, prevents recursive calls
        if message.author == self.user:
            return

        ## words for the bot to respond to as being not allowed in the server
        bad_words = [
            'cheat', 'cheats', 'hack', 'hacks', 'internal', 'external', 'ddos',
            'denial of service'
        ]

        messageContent = message.content  # store the message in a string
        ## loop through the message looking for the key words
        if len(messageContent) > 0:  # make sure the message contains something
            for word in bad_words:
                if word in messageContent:
                    await message.delete()  # delete the message if bad_words
                    await message.channel.send('Do not say that!')

        ## keyword detection uses existing string methods to parse messages
        ## keyword commands for the bot to respond to, start with !
        if message.content.startswith('!hello'):
            await message.channel.send("Ello!", mention_author=True)

        ## can also check endswith to detect questions
        if message.content.endswith('hello?'):
            await message.reply("No, I said ello, but that's close enough.")

        ## Playing with random text selection
        if message.content.endswith('?magic8ball'):  # need to make sure the question ends with key word to trigger
            magicResponse = random.choice(
                ['It is certain', 'As i see it, yes', 'Dont count on it', 'Without a doubt', 'Definitely',
                 'Very doubtful', 'Outlook not so good', 'My sources say no', 'My reply is no', 'Most likely',
                 'You may rely on it', 'Ask again later'])
            await message.channel.send(magicResponse)

        # ## message commands to join and leave voice chat
        # if message.content == '!join':
        #     if not message.author.voice:
        #         await message.channel.send("{} is not connected to a voice channel".format(message.author.name))
        #         return
        #     else:
        #         channel = message.author.voice.channel
        #         await channel.connect()
        # if message.content == '!leave':
        #     voice_client = message.guild.voice_client
        #     if voice_client.is_connected():
        #         await voice_client.disconnect()
        #     else:
        #         await send("The bot is not connected to a voice channel.")

        # dice rolling functionality
        if message.content.startswith('!roll'):
            roll_sum = dieMain(messageContent)  # call dieRoller functions
            await message.channel.send(
                f"Result of {messageContent} is {roll_sum}"
            )

    # Greeting when new member joins the chat
    async def on_member_join(self, member):
        await member.create_dm()  # Next part will send a DM to the member that just joined the channe
        await member.dm_channel.send(
            f"Hi {member.name}, welcome to the mad house. Fancy a cuppa?"
        )


## Intents are like permissions for what the bot can do
intents = discord.Intents.all()
## This is the portiong that actually initializes and starts the bot
client = MyClient(intents=intents)
client.run(TOKEN)
