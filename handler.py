import discord
import os
import json

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from utils.utils import (
    normalize_names,
    json_names_normalization,
    get_exact_match,
    get_included_matches,
    get_top_similarities,
)
from custom_embed import CustomEmbed
from custom_buttons import CustomButtons


MAX_POSSIBLE_CHOICES = 25


async def magic_autocomplete(interaction: discord.Interaction, current: str):
    normalized_current = normalize_names(current)
    choices = [
        app_commands.Choice(name=magic.get("nome"), value=magic.get("nome"))
        for magic in magic_json
        if normalized_current in magic.get("normalized_name")
    ]
    if len(choices) > MAX_POSSIBLE_CHOICES:
        return choices[:MAX_POSSIBLE_CHOICES]
    return choices


async def status_autocomplete(interaction: discord.Interaction, current: str):
    normalized_current = normalize_names(current)
    choices = [
        app_commands.Choice(name=status.get("nome"), value=status.get("nome"))
        for status in status_json
        if normalized_current in status.get("normalized_name")
    ]
    if len(choices) > MAX_POSSIBLE_CHOICES:
        return choices[:MAX_POSSIBLE_CHOICES]
    return choices


async def maneuver_autocomplete(interaction: discord.Interaction, current: str):
    normalized_current = normalize_names(current)
    choices = [
        app_commands.Choice(name=maneuver.get("nome"), value=maneuver.get("nome"))
        for maneuver in maneuver_json
        if normalized_current in maneuver.get("normalized_name")
    ]
    if len(choices) > MAX_POSSIBLE_CHOICES:
        return choices[:MAX_POSSIBLE_CHOICES]
    return choices


async def ally_autocomplete(interaction: discord.Interaction, current: str):
    normalized_current = normalize_names(current)
    choices = [
        app_commands.Choice(name=ally.get("nome"), value=ally.get("nome"))
        for ally in ally_json
        if normalized_current in ally.get("normalized_name")
    ]
    if len(choices) > MAX_POSSIBLE_CHOICES:
        return choices[:MAX_POSSIBLE_CHOICES]
    return choices


def pre_run_operations() -> tuple[dict]:
    global magic_json, status_json, maneuver_json, ally_json

    magic_file = open("data/magias.json")
    status_file = open("data/condicoes.json")
    maneuver_file = open("data/manobras.json")
    ally_file = open("data/parceiros.json")

    magic_json = json.loads(magic_file.read())
    status_json = json.loads(status_file.read())
    maneuver_json = json.loads(maneuver_file.read())
    ally_json = json.loads(ally_file.read())

    magic_json = json_names_normalization(magic_json)
    status_json = json_names_normalization(status_json)
    maneuver_json = json_names_normalization(maneuver_json)
    ally_json = json_names_normalization(ally_json)

    magic_file.close()
    status_file.close()
    maneuver_file.close()
    ally_file.close()


def handler():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents().default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="/", intents=intents)

    pre_run_operations()

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")
        await bot.tree.sync()

    @bot.tree.command(name="magias", description="Busque uma magia pelo nome")
    @app_commands.describe(magia="Nome da magia desejada")
    @app_commands.autocomplete(magia=magic_autocomplete)
    async def search_magic(interaction: discord.Interaction, *, magia: str):
        result_match = get_exact_match(magic_json, magia)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(magic_json, magia)
            if len(result_match) <= 0:
                result_match = get_top_similarities(magic_json, magia)

        custom_embed = CustomEmbed(result_match, "magic")
        main_embed = custom_embed.create_description_embed()
        if exact_match:
            await interaction.response.send_message(embed=main_embed)
        else:
            if len(result_match) > 0:
                buttonsView = CustomButtons(result_match, "magic", None)
                await interaction.response.send_message(
                    embed=main_embed, view=buttonsView
                )
            else:
                await interaction.response.send_message(embed=main_embed)

    @bot.tree.command(name="condicoes", description="Busque uma condição pelo nome")
    @app_commands.describe(condicao="Nome da condição desejada")
    @app_commands.autocomplete(condicao=status_autocomplete)
    async def search_status(interaction: discord.Interaction, *, condicao: str):
        result_match = get_exact_match(status_json, condicao)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(status_json, condicao)
            if len(result_match) <= 0:
                result_match = get_top_similarities(status_json, condicao)

        custom_embed = CustomEmbed(result_match, "status")
        main_embed = custom_embed.create_description_embed()
        if exact_match:
            related_status = result_match.get("condicoes_relacionadas")
            if related_status:
                related_embed = custom_embed.create_related_items_embed()
                buttonsView = CustomButtons(related_status, "status", status_json)
                await interaction.response.send_message(
                    embeds=[main_embed, related_embed], view=buttonsView
                )
            else:
                await interaction.response.send_message(embed=main_embed)
        else:
            if len(result_match) > 0:
                buttonsView = CustomButtons(result_match, "status", None)
                await interaction.response.send_message(
                    embed=main_embed, view=buttonsView
                )
            else:
                await interaction.response.send_message(embed=main_embed)

    @bot.tree.command(
        name="manobras", description="Busque uma manobra de combate pelo nome"
    )
    @app_commands.describe(manobra="Nome da manobra de combate desejada")
    @app_commands.autocomplete(manobra=maneuver_autocomplete)
    async def search_maneuver(interaction: discord.Interaction, *, manobra: str):
        result_match = get_exact_match(maneuver_json, manobra)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(maneuver_json, manobra)
            if len(result_match) <= 0:
                result_match = get_top_similarities(maneuver_json, manobra)

        custom_embed = CustomEmbed(result_match, "maneuver")
        main_embed = custom_embed.create_description_embed()
        if exact_match:
            await interaction.response.send_message(embed=main_embed)
        else:
            if len(result_match) > 0:
                buttonsView = CustomButtons(result_match, "maneuver", None)
                await interaction.response.send_message(
                    embed=main_embed, view=buttonsView
                )
            else:
                await interaction.response.send_message(embed=main_embed)

    @bot.tree.command(name="parceiros", description="Busque um parceiro pelo nome")
    @app_commands.describe(parceiro="Nome do parceiro desejado")
    @app_commands.autocomplete(parceiro=ally_autocomplete)
    async def search_ally(interaction: discord.Interaction, *, parceiro: str):
        result_match = get_exact_match(ally_json, parceiro)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(ally_json, parceiro)
            if len(result_match) <= 0:
                result_match = get_top_similarities(ally_json, parceiro)

        custom_embed = CustomEmbed(result_match, "ally")
        main_embed = custom_embed.create_description_embed()
        if exact_match:
            await interaction.response.send_message(embed=main_embed)
        else:
            if len(result_match) > 0:
                buttonsView = CustomButtons(result_match, "ally", None)
                await interaction.response.send_message(
                    embed=main_embed, view=buttonsView
                )
            else:
                await interaction.response.send_message(embed=main_embed)

    bot.run(TOKEN)


if __name__ == "__main__":
    handler()
