import discord

from discord import app_commands
from utils.utils import normalize_names
from pre_run_tasks import PreRunTasks


class CustomAutoComplete:
    MAX_POSSIBLE_CHOICES = 25

    def __init__(self, pre_run_tasks: PreRunTasks) -> None:
        self.pre_run_tasks = pre_run_tasks

    async def magic_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice]:
        normalized_current = normalize_names(current)
        choices = [
            app_commands.Choice(name=magic.get("nome"), value=magic.get("nome"))
            for magic in self.pre_run_tasks.magic_json
            if normalized_current in magic.get("normalized_name")
        ]
        if len(choices) > self.MAX_POSSIBLE_CHOICES:
            return choices[: self.MAX_POSSIBLE_CHOICES]
        return choices

    async def status_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice]:
        normalized_current = normalize_names(current)
        choices = [
            app_commands.Choice(name=status.get("nome"), value=status.get("nome"))
            for status in self.pre_run_tasks.status_json
            if normalized_current in status.get("normalized_name")
        ]
        if len(choices) > self.MAX_POSSIBLE_CHOICES:
            return choices[: self.MAX_POSSIBLE_CHOICES]
        return choices

    async def maneuver_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice]:
        normalized_current = normalize_names(current)
        choices = [
            app_commands.Choice(name=maneuver.get("nome"), value=maneuver.get("nome"))
            for maneuver in self.pre_run_tasks.maneuver_json
            if normalized_current in maneuver.get("normalized_name")
        ]
        if len(choices) > self.MAX_POSSIBLE_CHOICES:
            return choices[: self.MAX_POSSIBLE_CHOICES]
        return choices

    async def ally_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice]:
        normalized_current = normalize_names(current)
        choices = [
            app_commands.Choice(name=ally.get("nome"), value=ally.get("nome"))
            for ally in self.pre_run_tasks.ally_json
            if normalized_current in ally.get("normalized_name")
        ]
        if len(choices) > self.MAX_POSSIBLE_CHOICES:
            return choices[: self.MAX_POSSIBLE_CHOICES]
        return choices
