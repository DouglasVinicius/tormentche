import discord
import os

from discord.ext import commands
from dotenv import load_dotenv


def handler():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents().default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="?", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")

    bot.run(TOKEN)


if __name__ == "__main__":
    handler()
