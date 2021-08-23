from discord.ext import commands
from main import client

class LoadCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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

def setup(bot):
    empty=0