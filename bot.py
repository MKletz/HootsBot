# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

description = "Discord bot for organizing tournaments"

bot = commands.Bot(command_prefix=":", description=description)

__version__ = "0.0.1"


cog_registry = [
    "cogs.match"
]


# On startup
@bot.event
async def on_ready() -> None:
    """
    on_ready is the a start up function that is called when the bots is started.
    displays information about the bot and the server it joins and loads cogs
    :return: None
    """
    for guild in bot.guilds:
        print(f'{bot.user} is connected to {guild.name}')
    print('Logged in as')
    print(f'Bot-Name: {bot.user.name}')
    print(f'Bot-ID: {bot.user.id}')
    # print(f'Dev Mode: {bot.dev}')
    print(f'Discord Version: {discord.__version__}')
    print(f'Bot Version: {__version__}')
    bot.AppInfo = await bot.application_info()
    print(f'Owner: {bot.AppInfo.owner}')
    print('------')
    for cog in cog_registry:
        try:
            bot.load_extension(cog)
            print(f"Loading cog: {cog}")
        except Exception as e:
            print(f'Couldn\'t load cog {cog}: {e}')


@bot.event
async def on_message(message) -> None:
    """
    on_message is a function to process all messages the bot sees.
    This is triggered on every message.
    :param message: discord message object
    :return: None
    """
    await bot.process_commands(message)

# Run Bot
if __name__ == "__main__":
    bot.run(TOKEN)
