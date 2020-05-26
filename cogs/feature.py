import os
import discord
import time
import asyncio
from discord.ext import commands

FEATURE_LANDING_CHANNEL = os.getenv('FEATURE_LANDING_CHANNEL')
FEATURE_COUNT = int(os.getenv('FEATURE_COUNT'))
FEATURE_CHANNEL_PREFIX = os.getenv('FEATURE_CHANNEL_PREFIX')
FEATURE_NOTIFICATION_INTERVAL = int(os.getenv('FEATURE_NOTIFICATION_INTERVAL'))
FEATURE_NOTIFICATION_MAX_WAIT = int(os.getenv('FEATURE_NOTIFICATION_MAX_WAIT'))
TOURNAMENT_ORGANIZER_ROLE = os.getenv('TOURNAMENT_ORGANIZER_ROLE')
TOURNAMENT_PLAYER_ROLE = os.getenv('TOURNAMENT_PLAYER_ROLE')

class Feature(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_role(TOURNAMENT_ORGANIZER_ROLE)
    async def feature(self, ctx) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid feature command. Supported commands are:\nmatch\nreset')

    async def notify_players(self,ctx,landing_channel,members) -> int:
        """
        notify_players mentions players not currently in the FEATURE_LANDING_CHANNEL to get there. Returns a count of messages it sent.
        :param ctx: discord context object
        :param landing_channel: voice_channel object for the FEATURE_LANDING_CHANNEL
        :param members: discord users to notify if they are not in the landing_channel
        :return: int
        """
        missing_members = []

        for member in members:
            if member not in landing_channel.members:
                missing_members.append(member)

        for member in missing_members:
            await ctx.message.channel.send(f'{member.mention} report to {landing_channel.name} immediately or risk disqualification.')
            await member.send(f'Report to {landing_channel.name} in {ctx.guild.name} immediately or risk disqualification.')

        return len(missing_members)

    @feature.command()
    async def reset(self, ctx) -> None:
        """
        feature_reset takes the members in the feature match channels and moved the back to the landing channel
        :param ctx: discord context object
        :return: None
        """
        landing_channel = discord.utils.get(ctx.message.guild.voice_channels, name=FEATURE_LANDING_CHANNEL)

        for feature_channel_id in range(1, (FEATURE_COUNT + 1)):
            for feature_channel_half in ['a', 'b']:
                feature_channel = discord.utils.get(ctx.message.guild.voice_channels,
                                                    name=f'{FEATURE_CHANNEL_PREFIX}{feature_channel_id}{feature_channel_half}')
                for member in feature_channel.members:
                    await member.move_to(landing_channel)

    @feature.command()
    async def match(self, ctx) -> None:
        """
        feature_match moves members from the landing channel to their respective feature match channels
        :param ctx: discord context object
        :return: None
        """
        if len(ctx.message.mentions) != 2:
            await ctx.message.channel.send('Please mention exactly two users for the :feature_match command. Example:\n:feature_match @PlayerA @PlayerB 2')
            return
 
        landing_channel = discord.utils.get(ctx.message.guild.voice_channels, name=FEATURE_LANDING_CHANNEL)

        time_waited = 0
        failed_to_fire = False

        while (await self.notify_players(ctx,landing_channel,ctx.message.mentions) != 0):
            await asyncio.sleep(FEATURE_NOTIFICATION_INTERVAL)
            time_waited += FEATURE_NOTIFICATION_INTERVAL
            if time_waited >= FEATURE_NOTIFICATION_MAX_WAIT:
                failed_to_fire = True
                break

        if failed_to_fire:
            to_role = discord.utils.get(ctx.message.guild.roles, name=TOURNAMENT_ORGANIZER_ROLE)
            await ctx.message.channel.send(f'{to_role.mention} feature match for {ctx.message.mentions[0].mention} and {ctx.message.mentions[1].mention} has failed to fire.')
            return
        
        #this dictionary is used to map index of mentions in command to which half of the feature match they are.
        match_dict = {
            'a': 0,
            'b': 1
        }

        feature_channel_id = ctx.message.content[-1]

        for feature_channel_half in match_dict.keys():
            #finds the channel fore half of a feature match. Ex: Feature1a or Feature1b.
            feature_channel = discord.utils.get(ctx.message.guild.voice_channels, name=f'{FEATURE_CHANNEL_PREFIX}{feature_channel_id}{feature_channel_half}')
            #empties the channel found above because there should only be the user we're moving in present.
            for member in feature_channel.members:
                await member.move_to(landing_channel)
            #moves a mentioned user into the feature channel
            member = ctx.message.mentions[match_dict[feature_channel_half]]
            await member.move_to(feature_channel)

def setup(bot):
    bot.add_cog(Feature(bot))