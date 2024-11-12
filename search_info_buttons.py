import discord
import builtins

from discord.ui import Button, View
from abstract_search_info import AbstractSearchInfo


class SearchInfoButtons(View):
    def __init__(
        self, buttons_values: list[dict], search_info: AbstractSearchInfo
    ) -> None:
        super().__init__()
        self.buttons_values = buttons_values
        self.search_info = search_info

        for index, value in enumerate(self.buttons_values):
            button = Button(
                label=value.get("nome"),
                custom_id=str(index),
                style=discord.ButtonStyle.danger,
            )
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, interation: discord.Interaction) -> None:
        embed = self.search_info.create_embeds(
            self.buttons_values[int(interation.data["custom_id"])]
        )

        # Avoid get related status recursion
        if type(embed) == builtins.list:
            embed = embed[0]
        await interation.response.send_message(embed=embed)
