import discord
from discord.ui import Button, View
from search_info_embed import SearchInfoEmbed


class SearchInfoButtons(View):
    def __init__(
        self,
        buttons_infos: list[dict],
        embed_type: str,
        related_json: list[dict] | None,
    ) -> None:
        super().__init__()
        self.related_json = related_json
        self.embed_type = embed_type
        self.buttons_infos = buttons_infos
        self.__normalize_input_buttons_infos()

        for index, button_info in enumerate(self.buttons_infos):
            button = Button(
                label=button_info.get("nome"),
                custom_id=str(index),
                style=discord.ButtonStyle.danger,
            )
            button.callback = self.button_callback
            self.add_item(button)

    async def button_callback(self, interation: discord.Interaction) -> None:
        response_embed = SearchInfoEmbed(
            self.buttons_infos[int(interation.data["custom_id"])], self.embed_type
        )
        await interation.response.send_message(
            embed=response_embed.create_description_embed()
        )

    def __normalize_input_buttons_infos(self) -> None:
        if self.buttons_infos[0].get("index"):
            normalized_buttons_infos = []
            for button_info in self.buttons_infos:
                normalized_buttons_infos.append(
                    self.related_json[button_info.get("index")]
                )
            self.buttons_infos = normalized_buttons_infos
