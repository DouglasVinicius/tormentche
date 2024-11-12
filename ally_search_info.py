import discord
import datetime

from abstract_search_info import AbstractSearchInfo


class AllySearchInfo(AbstractSearchInfo):
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

        variant = self.match_values.get("variante")
        embed.add_field(name="Variante", value=variant, inline=True)

        size = self.match_values.get("tamanho")
        if size:
            embed.add_field(name="Tamanho", value=size, inline=True)

        level = self.match_values.get("niveis")
        embed.add_field(name="\nNíveis", value="", inline=False)

        beginner = level.get("iniciante")
        embed.add_field(
            name="Iniciante",
            value=beginner,
            inline=True,
        )

        veteran = level.get("veterano")
        embed.add_field(
            name="Veterano",
            value=veteran,
            inline=True,
        )

        master = level.get("mestre")
        embed.add_field(
            name="Mestre",
            value=master,
            inline=True,
        )

        observations = self.match_values.get("observacoes")
        if observations:
            embed.add_field(
                name="*Observações*", value=f"*{observations}*", inline=False
            )

        embed.set_footer(
            text=f'{self.match_values.get("livro")}, Página {self.match_values.get("pagina")}',
            icon_url=None,
        )

        return embed

    def _create_sugestions_embed(self) -> discord.Embed:
        title = "Parceiro não encontrado"
        description = "Não foi possível encontrar o parceiro desejado. \
            Abaixo estão alguns outros parceiros similares que podem ser do seu interesse.\n\
            Caso encontre o desejado, apenas clique no botão correspondente."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed

    def _create_none_sugestions_embed(self) -> discord.Embed:
        title = "Parceiro não encontrado"
        description = "Não foi possível encontrar o parceiro desejado ou qualquer outro semelhante.\n\
            Por favor, digite corretamente o nome do parceiro."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed
