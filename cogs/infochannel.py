import discord
from discord import role
from discord.ext.commands.bot import Bot
from discord.utils import get
from discord.ext import commands
from main import client
import json

with open('config.json', 'r') as file_object:  
    config_file = json.load(file_object)
with open('save.json', 'r') as file_object:
    save_file = json.load(file_object)

statsCategoryID = config_file['statsCategoryID']
comBotRoleID = config_file['comBotRoleID']

communityBots = 0

class Infochannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @client.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def infochannel(ctx, arg):
        if arg == 'init' :
            await icInit(ctx)
        elif arg == 'update' :
            await icUpdate(ctx)
        elif arg == 'remove' :
            await icRemove(ctx)


    @commands.Cog.listener()
    async def on_ready(self):
        print("cog Infochannel loaded")
    
    

def setup(bot):
    empty = 0
    #bot.add_cog(Infochannel(bot))


async def icInit(ctx):
    global theInfochannel
    await communityBotsCount(ctx)
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
        guild.get_role(877973435748331591): discord.PermissionOverwrite(view_channel=True, connect=False)
    }
    theInfochannel = await get(guild.categories, id=statsCategoryID).create_voice_channel(name='Ragbot displays : {}'.format(communityBots), overwrites=overwrites)
    save_file['infochannelID'] = theInfochannel.id
    saveData()
    await ctx.reply(':white_check_mark: infochannel créé !')
    print('infochannel created')

async def icUpdate(ctx):
    await communityBotsCount(ctx)
    await ctx.guild.get_channel(save_file['infochannelID']).edit(name='Ragbot displays : {}'.format(communityBots))
    await ctx.reply(':white_check_mark: infochannel mis à jour !')
    print('infochannel updated')

async def icRemove(ctx):
    await ctx.guild.get_channel(save_file['infochannelID']).delete(reason='command \'infochannel remove\' used by {}'.format(ctx.author))
    await ctx.reply(':white_check_mark: infochannel supprimé !')
    print('infochannel removed')

async def communityBotsCount(ctx):
    global communityBots
    communityBots = 0
    async for member in ctx.guild.fetch_members(limit=None) :
        if get(ctx.guild.roles, id=comBotRoleID) in member.roles :
            communityBots += 1
    print('community bots : {}'.format(communityBots))

def saveData():
    with open('save.json', 'w') as file_object:
        json.dump(save_file, file_object)
        file_object.close()

