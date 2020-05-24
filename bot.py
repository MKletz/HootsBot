# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{client.user} is connected to {guild.name}')

@client.event
async def on_message(message):    
    if message.content.startswith('reset features'):
        landing_channel = discord.utils.get(message.guild.voice_channels, name=f'OpenFeatures')
        
        for feature_channel_id in ['1','2','3']:
            for feature_channel_half in ['a','b']:
                feature_channel = discord.utils.get(message.guild.voice_channels, name=f'Feature{feature_channel_id}{feature_channel_half}')
                for member in feature_channel.members:
                    await member.move_to(landing_channel)

    if message.content.startswith('feature match'):
        feature_channel_id = message.content[-1]
        landing_channel = discord.utils.get(message.guild.voice_channels, name=f'OpenFeatures')

        match_dict = {
            'a':0,
            'b':1
        }

        for feature_channel_half in match_dict.keys():
            feature_channel = discord.utils.get(message.guild.voice_channels, name=f'Feature{feature_channel_id}{feature_channel_half}')
            for member in feature_channel.members:
                await member.move_to(landing_channel)
            member = message.mentions[match_dict[feature_channel_half]]
            await member.move_to(feature_channel)

client.run(TOKEN)