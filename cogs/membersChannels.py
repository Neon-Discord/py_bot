import discord
from discord.ext import commands
from main import client
import json
import asyncio

# open the save file
with open('save_memberschannels.json') as file_object:
    save_file = json.load(file_object)

class MembersChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # the command
    @client.command()
    async def myChannel(ctx, action=None):
        if action == 'new' or action == 'create': # if the argument is 'new' or 'create'
            await newMemberChannel(ctx) # process the member channel creation

        elif action == 'del' or action == 'delete': # if the argument is 'del' or 'delete'
            await delMemberChannel(ctx) # process the member channel deletion

        elif action == None: # if there isn't any argument
            await ctx.reply("<:kannaWhat:889105008916824074> Un argument est attendu pour `myChannel` : \n - `new` ou `create` pour créer un salon \n - `delete` ou `del` pour supprimer votre salon")

        else: # if the argument isn't correct
            await ctx.reply("<:kannaWhat:889105008916824074> Les arguments pour `myChannel` sont : \n - `new` ou `create` pour créer un salon \n - `delete` ou `del` pour supprimer votre salon")

def setup(bot):
    None


async def newMemberChannel(ctx):
    # check if the author already has a channel
    for id in save_file: # check all the keys in the save dictionnary
        if id == str(ctx.author.id): # if the right key is found
            return await ctx.reply('Vous avez déja un salon à vous ! <:kannaWhat:889105008916824074>') # warning message
    
    # only the owner of the channel can see it and manage it
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True, manage_channels=True, manage_permissions=True, manage_webhooks=True, manage_messages=True)
    }

    category = discord.utils.get(ctx.guild.categories, id=888866728241692790)
    newChannel = await ctx.guild.create_text_channel(name=f'salon de {ctx.author.name}', overwrites=overwrites, category=category) # create the channel
    save_file[str(ctx.author.id)] = newChannel.id # register the channel in the json file
    saveData() # save the json file
    await ctx.reply(f'Voilà un salon rien que pour vous : {newChannel.mention} ! <:mcHeart:889104967498072064>') # confirmation message
    print(f'new member channel for <{ctx.author}>') # confirmation in console


async def delMemberChannel(ctx):
    # check if the autor has a channel
    hasChannel = False
    for id in save_file: # check all the keys in the save dictionnary
        if id == str(ctx.author.id): # if the right key is found
            hasChannel = True # confirm that the author has a channel
            break # break the for loop
    if hasChannel == False:
        return await ctx.reply("Vous n'avez pas encore de salon personnel... <:kannaWhat:889105008916824074>") # message if haven't a channel already

    # ask for confirmation
    msg = await ctx.reply("Êtes vous vraiment sûr de vouloir supprimer votre salon personnel ? <:pablo:889105016839888896> \n*Vous avez 10 secondes pour confirmer ou annuler.*")

    # add reactions to the message
    emojis = ['✅', '❌']
    for emoji in emojis:
        await msg.add_reaction(emoji)

    # check if the reaction is correct and is from the author
    reacted = None
    def check(reaction, user):
        reacted = reaction.emoji
        return user.id == ctx.author.id and str(reaction.emoji) in emojis

    # wait for reaction
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=10, check=check) # wait 10sec for a reaction
    except asyncio.TimeoutError:
        await ctx.send(f"{ctx.author.mention} le temps est écoulé, suppression annulée.") # timeout message
    else:
        # check the reaction
        if str(reaction.emoji) == '✅':
            for id in save_file: # check all the keys in the dictionnary
                if id == str(ctx.author.id): # if the right key is found in the dictionnary
                    await client.get_channel(save_file[id]).delete() # delete the channel
                    del save_file[str(ctx.author.id)] # remove the reference in the json file
                    saveData() # save the json file
                    break # break the for loop
            await ctx.send(f"{ctx.author.mention} Votre salon a bien été supprimé !") # confirmation message for deleting
            print(f'<{ctx.author}> has deleted his member channel')

        elif str(reaction.emoji) == '❌':
            await ctx.send(f"{ctx.author.mention} Vous avez annulé !") # confirmation message for canceling

        else:
            await ctx.send(f"{ctx.author.mention} Une erreur est survenue... Suppression annulée.") # if the reaction isn't CheckMark or CrossMark send an error message

# saving function
def saveData():
    global save_file

    # write in the file
    with open('save_memberschannels.json', 'w') as file_object:
        json.dump(save_file, file_object)
        file_object.close()
    
    # re-open the file to update the dictionnary
    with open('save_memberschannels.json') as file_object:
        save_file = json.load(file_object)