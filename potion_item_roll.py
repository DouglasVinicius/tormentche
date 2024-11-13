import discord
import datetime

from abstract_item_roll import AbstractItemRoll


class PotionItemRoll(AbstractItemRoll):
    def _get_items(self) -> list[dict]:
        return self.json_data.get("pocoes")

    def create_embeds(
        self, rolled_items: list[dict]
    ) -> list[discord.Embed] | discord.Embed:
        embed = discord.Embed(
            title="Poções",
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )
        embed.set_author(name=self.json_data.get("titulo"), url=None, icon_url=None)

        for rolled_item in rolled_items:
            embed.add_field(
                name=rolled_item.get("item").get("nome"),
                value=f"Preço: {rolled_item.get('item').get('preco')}, Resultado do dado: {rolled_item.get('roll')}",
                inline=False,
            )

        embed.set_footer(
            text=f'{self.json_data.get("livro")}, Página {self.json_data.get("pagina")}',
            icon_url=None,
        )

        return embed
