import discord
import datetime

from abstract_item_roll import AbstractItemRoll


class ChaosDeckItemRoll(AbstractItemRoll):
    def _get_items(self) -> list[dict]:
        return self.json_data.get("cartas")

    def create_embeds(
        self, rolled_items: list[dict]
    ) -> list[discord.Embed] | discord.Embed:
        embed = discord.Embed(
            title=self.json_data.get("titulo"),
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        for rolled_item in rolled_items:
            embed.add_field(
                name=f"{rolled_item.get('roll')} - {rolled_item.get('item').get('nome')}",
                value=rolled_item.get("item").get("efeito"),
                inline=False,
            )

        embed.set_footer(
            text=f'{self.json_data.get("livro")}, Página {self.json_data.get("pagina")}',
            icon_url=None,
        )

        return embed
