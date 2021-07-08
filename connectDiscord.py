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
## import for handling .env files, .env files store credentials
from dotenv import load_dotenv

load_dotenv()
## Discord token read into program from an environment variable for security
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

## client represents connection to discord, similar to a sftp object
## handles events, tracks state, and interacts with Discord APIs
client = discord.Client()

""" Here the @client.events handle everything that the bot reacts to in the server"""

@client.event
async def on_ready():
    for guild in client.guilds: # loop through client.guilds data matching for guild name in .env
        if guild.name == GUILD:
        break
    print(f'{client.user} has connected to the following server:')  # print the bots name
    print(f'{guild.name}(id: {guild.id})')  # print the server name and id

    ## Print out the members of the server
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')  # Only prints the bots name for some reason

    ## Greeting when new member joins the chat
    @client.event
    async def on_member_join(member):
        await member.create_dm()    # Next part will send a DM to the member that just joined the channel
        await member.dm_channel.send(
            f'Ello {member.name}, lovely server innit!'
        )

client.run(TOKEN)
