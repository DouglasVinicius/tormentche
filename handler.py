import discord
import os
import builtins

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from abstract_search_info_embed import AbstractSearchInfoEmbed
from help_embed import HelpEmbed
from status_search_info_embed import StatusSearchInfoEmbed
from magic_search_info_embed import MagicSearchInfoEmbed
from maneuver_search_info_embed import ManeuverSearchInfoEmbed
from ally_search_info_embed import AllySearchInfoEmbed
from search_info_buttons import SearchInfoButtons
from search_info_auto_complete import SearchInfoAutoComplete
from dice_roll import DiceRoll
from pre_run_tasks import PreRunTasks


async def send_search_info_message(
    interaction: discord.Interaction,
    search_info_embed: AbstractSearchInfoEmbed,
    json_data: list[dict],
    input: str,
) -> None:
    match_values = search_info_embed.get_correct_match(input)
    embeds = search_info_embed.create_embeds(match_values)

    # If it is a list type, it means that is a exact match and have related status (have related status embed)
    if type(embeds) == builtins.list:
        related_status_values = [
            json_data[value.get("index")]
            for value in match_values.get("condicoes_relacionadas")
        ]
        search_info_buttons_view = SearchInfoButtons(
            related_status_values, search_info_embed
        )

        await interaction.response.send_message(
            embeds=embeds, view=search_info_buttons_view
        )
    else:
        if len(match_values) > 0 and type(match_values) == builtins.list:
            search_info_buttons_view = SearchInfoButtons(
                match_values, search_info_embed
            )
            await interaction.response.send_message(
                embed=embeds, view=search_info_buttons_view
            )
        else:
            await interaction.response.send_message(embed=embeds)


def handler() -> None:
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents().default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="?", intents=intents)

    pre_run_tasks = PreRunTasks()
    magic_search_info_auto_complete = SearchInfoAutoComplete(pre_run_tasks.magic_json)
    status_search_info_auto_complete = SearchInfoAutoComplete(pre_run_tasks.status_json)
    maneuver_search_info_auto_complete = SearchInfoAutoComplete(
        pre_run_tasks.maneuver_json
    )
    ally_search_info_auto_complete = SearchInfoAutoComplete(pre_run_tasks.ally_json)

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user.name}")

    @bot.command()
    @commands.is_owner()
    async def sync(ctx: commands.Context) -> None:
        await bot.tree.sync()
        await ctx.send("Comandos sincronizados com sucesso!")

    @bot.tree.command(
        name="ajuda", description="Informa os possíveis comandos e suas utilizações."
    )
    async def help_command(interaction: discord.Interaction) -> None:
        help_embed = HelpEmbed()
        await interaction.response.send_message(embed=help_embed.create_help_embed())

    @bot.tree.command(name="magias", description="Busque uma magia pelo nome.")
    @app_commands.describe(magia="Nome da magia desejada.")
    @app_commands.autocomplete(magia=magic_search_info_auto_complete.autocomplete)
    async def search_magic(interaction: discord.Interaction, *, magia: str) -> None:
        magic_search_info_embed = MagicSearchInfoEmbed(pre_run_tasks.magic_json)
        await send_search_info_message(
            interaction, magic_search_info_embed, pre_run_tasks.magic_json, magia
        )

    @bot.tree.command(name="condicoes", description="Busque uma condição pelo nome.")
    @app_commands.describe(condicao="Nome da condição desejada.")
    @app_commands.autocomplete(condicao=status_search_info_auto_complete.autocomplete)
    async def search_status(interaction: discord.Interaction, *, condicao: str) -> None:
        status_search_info_embed = StatusSearchInfoEmbed(pre_run_tasks.status_json)
        await send_search_info_message(
            interaction, status_search_info_embed, pre_run_tasks.status_json, condicao
        )

    @bot.tree.command(
        name="manobras", description="Busque uma manobra de combate pelo nome."
    )
    @app_commands.describe(manobra="Nome da manobra de combate desejada.")
    @app_commands.autocomplete(manobra=maneuver_search_info_auto_complete.autocomplete)
    async def search_maneuver(
        interaction: discord.Interaction, *, manobra: str
    ) -> None:
        maneuver_search_info_embed = ManeuverSearchInfoEmbed(
            pre_run_tasks.maneuver_json
        )
        await send_search_info_message(
            interaction,
            maneuver_search_info_embed,
            pre_run_tasks.maneuver_json,
            manobra,
        )

    @bot.tree.command(name="parceiros", description="Busque um parceiro pelo nome.")
    @app_commands.describe(parceiro="Nome do parceiro desejado.")
    @app_commands.autocomplete(parceiro=ally_search_info_auto_complete.autocomplete)
    async def search_ally(interaction: discord.Interaction, *, parceiro: str) -> None:
        ally_search_info_embed = AllySearchInfoEmbed(pre_run_tasks.ally_json)
        await send_search_info_message(
            interaction, ally_search_info_embed, pre_run_tasks.ally_json, parceiro
        )

    @bot.tree.command(
        name="rolar",
        description="Rola dados e calcula o resultado de expressões matemáticas. Use a sintaxe '{NUM_DADOS}d{NUM_FACES}'.",
    )
    @app_commands.describe(
        expressao="A expressão matemática que inclui a rolagem de dados e/ou operações matemáticas."
    )
    async def roll_dice(interaction: discord.Interaction, *, expressao: str) -> None:
        dice_roll = DiceRoll()
        normalized_expression, resolved_expression, roll_result = dice_roll.make_roll(
            expressao
        )

        embed = dice_roll.create_embed(
            normalized_expression, resolved_expression, roll_result
        )
        await interaction.response.send_message(embed=embed)

    bot.run(TOKEN)


if __name__ == "__main__":
    handler()
