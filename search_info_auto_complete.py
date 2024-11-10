import discord

from discord import app_commands
from itertools import islice
from utils.utils import name_normalizer


class SearchInfoAutoComplete:
    def __init__(self, json_data: list[dict]) -> None:
        self.json_data = json_data

    async def autocomplete(
        self, interaction: discord.Interaction, input: str
    ) -> list[app_commands.Choice]:
        MAX_POSSIBLE_CHOICES = 25
        normalized_input = name_normalizer(input)

        choices = list(
            islice(
                (
                    app_commands.Choice(name=value.get("nome"), value=value.get("nome"))
                    for value in self.json_data
                    if normalized_input in value.get("normalized_name")
                ),
                MAX_POSSIBLE_CHOICES,
            )
        )
        return choices
