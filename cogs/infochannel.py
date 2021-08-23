import discord
from discord import role
from discord import colour
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
initState = False

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
    
    @commands.Cog.listener()
    async def on_member_update(before, after):
        print('member update')
        if after.guild.get_role(comBotRoleID) in (after.roles or before.roles):
            await communityBotsCount(after)

def setup(bot):
    empty = 0


async def icInit(ctx):
    await communityBotsCount(ctx)
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
        guild.get_role(877973435748331591): discord.PermissionOverwrite(view_channel=True, connect=False)
    }
    global initState
    initState = True

    embed = discord.Embed(title = 'Nouvel infochannel', color = discord.Color.orange())
    embed.add_field(name = 'Le texte', value = 'Tapez le texte que l\'infochannel va afficher ainsi que des @mentions de __rôles__ qui compteront le nombre de membre possédant ce/ces rôle.')
    
    await ctx.send(embed=embed)
    #theInfochannel = await get(guild.categories, id=statsCategoryID).create_voice_channel(name='Ragbot displays : {}'.format(communityBots), overwrites=overwrites)
    #save_file['infochannelID'] = theInfochannel.id
    #saveData()


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

