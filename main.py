import discord
from discord import guild
from discord import channel
from discord.channel import CategoryChannel
from discord.ext.commands import Bot
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
for intent in intents:
    print(intent)

load_dotenv()
token = getenv("TOKEN")

client = Bot(command_prefix='.', intents = intents)

print('- - -')
for file in os.listdir("./cogs"): # lists all the cog files inside the cog folder
    if file.endswith(".py"): # It gets all the cogs that ends with a ".py"
        name = file[:-3] # It gets the name of the file removing the ".py"
        client.load_extension(f"cogs.{name}") # This loads the cog
        print("cog loaded : ", name)



guildID = 876210790250741830
statsCategoryID = 878065627758207016
comBotRoleID = 878043146284580894
communityBots = 0
theInfochannel: discord.VoiceChannel

print('- - -')
with open('save.json', 'r') as file_object:  
  data = json.load(file_object)
print(type(data))
print(data)
data['infochannelID'] += 1
print(data['infochannelID'])


@client.event
async def on_ready():
    neonGuild = client.get_guild(guildID)
    print('- - -')
    print('We have logged in as {0.user} in these guilds :'.format(client))
    for guild in client.guilds :
        print('  - {}'.format(guild))
    
    print('- - -')
    async for member in neonGuild.fetch_members(limit=None) :
        global communityBots
        if get(guild.roles, id=comBotRoleID) in member.roles :
            communityBots += 1
    print('community bots : {}'.format(communityBots))

@client.command()
async def test(ctx):
    await ctx.reply('test')

@client.command()
async def load(ctx, *, name: str):
    try:
        client.load_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.reply(f'"**{name}**" Cog loaded')

@client.command()
async def reload(ctx, *, name: str):
    try:
        client.reload_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.reply(f'"**{name}**" Cog reloaded')

@client.command()
async def getuser(ctx, role: discord.Role):
    await ctx.reply("\n".join(str(role) for role in role.members))



client.run(token)