import discord
import os
import json

from discord.ext import commands
from dotenv import load_dotenv
from utils.utils import (
    json_names_normalization,
    get_exact_match,
    get_included_matches,
    get_top_similarities,
)
from custom_embed import CustomEmbed
from custom_buttons import CustomButtons


def pre_run_operations() -> tuple[dict]:
    magic_file = open("data/magias.json")

    magic_json = json.loads(magic_file.read())

    magic_json = json_names_normalization(magic_json)

    magic_file.close()

    return magic_json


def handler():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents().default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="?", intents=intents)

    magic_json = pre_run_operations()

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")

    @bot.command("buscar_magia")
    async def search_magic(ctx, *, message: str):
        result_match = get_exact_match(magic_json, message)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(magic_json, message)
            if len(result_match) <= 0:
                result_match = get_top_similarities(magic_json, message)

        custom_embed = CustomEmbed(result_match, "magic")
        main_embed = custom_embed.create_description_embed()
        if exact_match:
            await ctx.send(embed=main_embed)
        else:
            await ctx.send(embed=main_embed)
            if len(result_match) > 0:
                buttonsView = CustomButtons(result_match, "magic", None)
                await ctx.send(view=buttonsView)

    bot.run(TOKEN)


if __name__ == "__main__":
    handler()
