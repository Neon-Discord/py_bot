import discord
from discord import guild
from discord import channel
from discord.channel import CategoryChannel
from discord.client import Client
from discord.ext import commands
from discord.ext.commands.converter import clean_content
from discord.flags import Intents
from discord.member import Member
from discord.utils import get

from dotenv import load_dotenv
import os
from os import getenv

import json

intents = discord.Intents.default()
intents.members = True
intents.presences = True
for intent in intents:
    print(intent)

load_dotenv()
token = getenv("TOKEN")

client = commands.Bot(command_prefix='*', intents = intents)
theClient = Client(intents=intents)

print('- - -')
for file in os.listdir('./cogs'): # lists all the cog files inside the cog folder
    if file.endswith('.py'): # It gets all the cogs that ends with a ".py"
        name = file[:-3] # It gets the name of the file removing the ".py"
        client.load_extension(f'cogs.{name}') # This loads the cog
        print('cog loaded :', name)


guildID = 876210790250741830
statsCategoryID = 878065627758207016
comBotRoleID = 878043146284580894
communityBots = 0
theInfochannel: discord.VoiceChannel


@client.event
async def on_ready():
    neonGuild = client.get_guild(guildID)
    print('- - -')
    print('We have logged in as {0} in {1} guilds :'.format(client.user, len(client.guilds)))
    for guild in client.guilds :
        print('  - name: <{0}>  id: <{1}>'.format(guild, guild.id))
    print('- - -')

@client.command()
async def ragtest(ctx):
    await ctx.reply('test')



client.run(token)