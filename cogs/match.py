import discord
from discord.ext import commands


class Match(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reset_feature(self, ctx) -> None:
        """
        reset_feature takes the members in the feature match channels and moved the back to the landing channel
        :param ctx: discord context object
        :return: None
        """
        landing_channel = discord.utils.get(ctx.message.guild.voice_channels, name=f'OpenFeatures')

        for feature_channel_id in ['1', '2', '3']:
            for feature_channel_half in ['a', 'b']:
                feature_channel = discord.utils.get(ctx.message.guild.voice_channels,
                                                    name=f'Feature{feature_channel_id}{feature_channel_half}')
                if not feature_channel.members:
                    print("No Members found in feature channel")
                    return
                for member in feature_channel.members:
                    await member.move_to(landing_channel)

    @commands.command()
    async def feature_match(self, ctx) -> None:
        """
        feature_match moves members from the landing channel to their respective feature match channels
        :param ctx: discord context object
        :return: None
        """
        feature_channel_id = ctx.message.content[-1]
        landing_channel = discord.utils.get(ctx.message.guild.voice_channels, name=f'OpenFeatures')

        match_dict = {
            'a': 0,
            'b': 1
        }

        for feature_channel_half in match_dict.keys():
            feature_channel = discord.utils.get(ctx.message.guild.voice_channels, name=f'Feature{feature_channel_id}{feature_channel_half}')
            for member in feature_channel.members:
                await member.move_to(landing_channel)
            member = ctx.message.mentions[match_dict[feature_channel_half]]
            await member.move_to(feature_channel)


def setup(bot):
    bot.add_cog(Match(bot))
