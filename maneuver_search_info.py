import discord
import datetime

from abstract_search_info import AbstractSearchInfo


class ManeuverSearchInfo(AbstractSearchInfo):
    def create_embeds(
        self, match_values: dict | list[dict]
    ) -> list[discord.Embed] | discord.Embed:
        return super().create_embeds(match_values)

    def _create_exact_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=self.match_values.get("nome"),
            description=self.match_values.get("descricao"),
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        embed.set_footer(
            text=f'{self.match_values.get("livro")}, Página {self.match_values.get("pagina")}',
            icon_url=None,
        )

        return embed

    def _create_sugestions_embed(self) -> discord.Embed:
        title = "Manobra de combate não encontrada"
        description = "Não foi possível encontrar a manobra desejada. \
            Abaixo estão algumas outras manobras similares que podem ser do seu interesse.\n\
            Caso encontre a desejada, apenas clique no botão correspondente."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed

    def _create_none_sugestions_embed(self) -> discord.Embed:
        title = "Manobra de combate não encontrada"
        description = "Não foi possível encontrar a manobra desejada ou qualquer outra semelhante.\n\
            Por favor, digite corretamente o nome da manobra."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed
