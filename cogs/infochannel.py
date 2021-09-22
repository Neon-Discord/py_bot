import discord
from discord.ext import commands
from discord.ext.commands.core import check
from main import client
import json
import random

with open('config.json') as file_object:  
    config_file = json.load(file_object)
with open('save_infochannels.json') as file_object:
    save_file = json.load(file_object)

statsCategoryID = config_file['statsCategoryID']
comBotRoleID = config_file['comBotRoleID']

communityBots = 0
initState = 0


class Infochannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @client.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def abc(ctx):
        await ctx.reply('yes')
    
    @client.event
    async def on_member_update(before, after):
        if before.roles != after.roles or after.roles != before.roles:
            await icUpdate()

    @client.event
    async def on_member_join():
        await icUpdate()
    
    @client.event
    async def on_member_remove():
        await icUpdate()

def setup(bot):
    None


async def icUpdate():
    guild = client.get_guild(888866727562207283)

    for channel in save_file:

        count = 0

        if save_file[channel]['roleID'] == 'bot':
            for member in guild.members:
                if member.bot == True:
                    count += 1
        
        elif save_file[channel]['roleID'] == 'human':
            for member in guild.members:
                if member.bot == False:
                    count += 1

        else:
            members = guild.get_role(save_file[channel]['roleID']).members
            count = len(members)
        
        print('Infochannel <{0}> will be update to <{1}>'.format(save_file[channel]['text'], count))
        text = save_file[channel]['text'] + str(count) + save_file[channel]['textAfter']
        await client.get_channel(888866728241692791).send('**{0}** sera mis à jour : **{1}**'.format(save_file[channel]['text'], count))
        await client.get_channel(int(channel)).edit(name=text)
        await client.get_channel(888866728241692791).send('**{0}** a été mis à jour'.format(save_file[channel]['text']))


def saveData():
    with open('save.json', 'w') as file_object:
        json.dump(save_file, file_object)
        file_object.close()