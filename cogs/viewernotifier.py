import os
import discord
from discord.ext import tasks, commands

class ViewerNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild =  discord.utils.get(bot.guilds, name="Hooglandia")
        self.announcementChannel = discord.utils.get(self.guild.channels, name='announcements')
        self.ownerGame = ''
        self.gameRoledict = {
            'pauper':'MTGOLiveNotify',
            'vintage':'MTGOLiveNotify',
            'legacy':'MTGOLiveNotify',
            'modern':'MTGOLiveNotify',
            'standard':'ArenaLiveNotify',
            'historic':'ArenaLiveNotify',
            'runeterra':'RuneterraLiveNotify'
        }
        self.gameChange.start()

    def cog_unload(self):
        self.gameChange.cancel()

    @tasks.loop(seconds=5.0)
    async def gameChange(self):
        for activity in self.guild.owner.activities:
            key = activity.name.lower().split(':')[0]
            if self.ownerGame != key:
                self.ownerGame = key
                if None != self.gameRoledict[key]:
                    role = discord.utils.get(self.guild.roles, name=self.gameRoledict[key])
                    await self.announcementChannel.send(f'{role.mention} Jeff is playing {key}!')

def setup(bot):
    bot.add_cog(ViewerNotifier(bot))