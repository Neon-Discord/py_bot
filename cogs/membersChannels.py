import discord
from discord.ext import commands
from main import client
import json

with open('save_memberschannels.json') as file_object:
    save_file = json.load(file_object)

class MembersChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @client.command()
    async def myChannel(ctx, arg):
        if arg == 'new':
            await newMemberChannel(ctx)

def setup(bot):
    None


async def newMemberChannel(ctx):
    for id in save_file:
        if id == str(ctx.author.id):
            return await ctx.reply('Vous avez déja un salon à vous ! <:kannaWhat:889105008916824074>')
    
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True, manage_channels=True, manage_permissions=True, manage_webhooks=True, manage_messages=True)
    }
    newChannel = await ctx.guild.create_text_channel(name='salon de {}'.format(ctx.author.name), overwrites=overwrites)
    save_file['{}'.format(ctx.author.id)] = newChannel.id
    saveData()
    await ctx.reply('Voilà un salon rien que pour vous <#{}> ! <:mcHeart:889104967498072064>'.format(newChannel.id))
    print('new member channel for', ctx.author)


def saveData():
    with open('save_memberschannels.json', 'w') as file_object:
        json.dump(save_file, file_object)
        file_object.close()