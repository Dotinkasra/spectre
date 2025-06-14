from discord.ext import commands
import discord

import asyncio

from Source.env.config import Config


config = Config()
intents = discord.Intents.all()
TOKEN = config.token
guilds = config.guilds
bot = commands.Bot(command_prefix='h!', intents = intents)


async def main():
    INITIAL_EXTENSIONS = [
        'Source.cogs.voicechannel_log',
        'Source.cogs.auto_reaction',
        'Source.cogs.auto_ban',
    ]

    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)
    
    await bot.start(TOKEN)

asyncio.run(main())