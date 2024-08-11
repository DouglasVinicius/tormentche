import discord
import os

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from utils.utils import (
    get_exact_match,
    get_included_matches,
    get_top_similarities,
)
from custom_embed import CustomEmbed
from custom_buttons import CustomButtons
from custom_auto_complete import CustomAutoComplete
from pre_run_tasks import PreRunTasks


def handler() -> None:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents().default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="/", intents=intents)

    pre_run_tasks = PreRunTasks()
    custom_auto_complete = CustomAutoComplete(pre_run_tasks)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")
        await bot.tree.sync()

    @bot.tree.command(name="magias", description="Busque uma magia pelo nome")
    @app_commands.describe(magia="Nome da magia desejada")
    @app_commands.autocomplete(magia=custom_auto_complete.magic_autocomplete)
    async def search_magic(interaction: discord.Interaction, *, magia: str):
        result_match = get_exact_match(pre_run_tasks.magic_json, magia)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(pre_run_tasks.magic_json, magia)
            if len(result_match) <= 0:
                result_match = get_top_similarities(pre_run_tasks.magic_json, magia)

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
    @app_commands.autocomplete(condicao=custom_auto_complete.status_autocomplete)
    async def search_status(interaction: discord.Interaction, *, condicao: str):
        result_match = get_exact_match(pre_run_tasks.status_json, condicao)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(pre_run_tasks.status_json, condicao)
            if len(result_match) <= 0:
                result_match = get_top_similarities(pre_run_tasks.status_json, condicao)

        custom_embed = CustomEmbed(result_match, "status")
        main_embed = custom_embed.create_description_embed()
        if exact_match:
            related_status = result_match.get("condicoes_relacionadas")
            if related_status:
                related_embed = custom_embed.create_related_items_embed()
                buttonsView = CustomButtons(
                    related_status, "status", pre_run_tasks.status_json
                )
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
    @app_commands.autocomplete(manobra=custom_auto_complete.maneuver_autocomplete)
    async def search_maneuver(interaction: discord.Interaction, *, manobra: str):
        result_match = get_exact_match(pre_run_tasks.maneuver_json, manobra)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(pre_run_tasks.maneuver_json, manobra)
            if len(result_match) <= 0:
                result_match = get_top_similarities(
                    pre_run_tasks.maneuver_json, manobra
                )

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
    @app_commands.autocomplete(parceiro=custom_auto_complete.ally_autocomplete)
    async def search_ally(interaction: discord.Interaction, *, parceiro: str):
        result_match = get_exact_match(pre_run_tasks.ally_json, parceiro)
        exact_match = True

        if not result_match:
            exact_match = False
            result_match = get_included_matches(pre_run_tasks.ally_json, parceiro)
            if len(result_match) <= 0:
                result_match = get_top_similarities(pre_run_tasks.ally_json, parceiro)

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
