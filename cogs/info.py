import os
import discord
from discord.ext import commands

TOURNAMENT_URL = os.getenv('TOURNAMENT_URL')
TOURNAMENT_ARCHIVE = os.getenv('TOURNAMENT_ARCHIVE')

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    #@commands.has_role(TOURNAMENT_ORGANIZER_ROLE)
    async def info(self, ctx) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.message.author.send(f'General tournament information can be found here {TOURNAMENT_URL}')

    @info.command()
    async def archive(self, ctx) -> None:
        await ctx.message.author.send(f'Archives of coverage can be found here {TOURNAMENT_ARCHIVE}')


def setup(bot):
    bot.add_cog(Info(bot))