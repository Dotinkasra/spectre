from discord.ext import commands
from discord import app_commands
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
    ]

    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)
    
    await bot.start(TOKEN)

asyncio.run(main())