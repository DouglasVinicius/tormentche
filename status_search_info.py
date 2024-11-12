import discord
import datetime
import builtins

from typing import Literal
from abstract_search_info import AbstractSearchInfo


class StatusSearchInfo(AbstractSearchInfo):
    def create_embeds(
        self, match_values: dict | list[dict]
    ) -> list[discord.Embed] | discord.Embed:
        self.match_values = match_values
        embed_type = self._get_embed_type()

        if embed_type == "exact":
            if self.match_values.get("condicoes_relacionadas"):
                return [
                    self._create_description_embed(),
                    self._create_related_status_embed(),
                ]

        return self._create_description_embed()

    def _get_embed_type(self) -> Literal["exact", "sugestion", "none"]:
        match type(self.match_values):
            case builtins.dict:
                return "exact"
            case builtins.list:
                if len(self.match_values) > 0:
                    return "sugestion"
                else:
                    return "none"

    def _create_related_status_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="Condições relacionadas",
            description="As seguintes condições tem relação com a condição encontrada. \
                Caso queira visualizá-las também, clique no respectivo botão.",
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed

    def _create_exact_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=self.match_values.get("nome"),
            description=self.match_values.get("descricao"),
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        status_type = self.match_values.get("tipo")
        if status_type:
            embed.add_field(name="Tipo", value=status_type, inline=False)

        embed.set_footer(
            text=f'{self.match_values.get("livro")}, Página {self.match_values.get("pagina")}',
            icon_url=None,
        )

        return embed

    def _create_sugestions_embed(self) -> discord.Embed:
        title = "Condição não encontrada"
        description = "Não foi possível encontrar a condição desejada. \
            Abaixo estão algumas outras condições similares que podem ser do seu interesse.\n\
            Caso encontre a desejada, apenas clique no botão correspondente."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed

    def _create_none_sugestions_embed(self) -> discord.Embed:
        title = "Condição não encontrada"
        description = "Não foi possível encontrar a condição desejada ou qualquer outra semelhante.\n\
            Por favor, digite corretamente o nome da condição."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed
