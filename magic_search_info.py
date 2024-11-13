import discord
import datetime
import builtins

from abstract_search_info import AbstractSearchInfo


class MagicSearchInfo(AbstractSearchInfo):
    def _create_exact_embed(self) -> discord.Embed:
        INLINE_FIELDS = [
            {"key": "resistencia", "name": "Resistência"},
            {"key": "alvo", "name": "Alvo"},
            {"key": "alvos", "name": "Alvos"},
            {"key": "area", "name": "Área"},
            {"key": "efeito", "name": "Efeito"},
            {"key": "alvo_ou_area", "name": "Alvo ou Área"},
            {"key": "execucao", "name": "Execução"},
            {"key": "alcance", "name": "Alcance"},
            {"key": "duracao", "name": "Duração"},
        ]
        CREATURES_FIELDS = [
            {"key": "for", "name": "Força"},
            {"key": "des", "name": "Destreza"},
            {"key": "pv", "name": "Pontos de Vida"},
            {"key": "tipos", "name": "Tipos de Aliados"},
            {"key": "defesa", "name": "Defesa"},
            {"key": "dano", "name": "Dano"},
            {"key": "efeito_adicional", "name": "Efeito adicional"},
        ]

        embed = discord.Embed(
            title=self.match_values.get("nome"),
            description=self.match_values.get("descricao"),
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        classification = self.match_values.get("classificacao")
        circle = self.match_values.get("circulo")
        school = self.match_values.get("escola")
        embed.set_author(
            name=f"{classification} {circle}, {school}",
            url=None,
            icon_url=None,
        )

        upgrades = self.match_values.get("aprimoramentos")
        for upgrade in upgrades:
            embed.add_field(
                name=upgrade.get("custo"),
                value=upgrade.get("descricao"),
                inline=False,
            )

        creatures = self.match_values.get("criaturas")
        if creatures:
            embed.add_field(name="\nEstatística das Criaturas", value="", inline=False)
            for creature in creatures:
                creature_description = ""
                for field in CREATURES_FIELDS:
                    value = creature.get(field.get("key"))
                    match type(value):
                        case builtins.str | builtins.int:
                            creature_description += (
                                f"**{field.get('name')}:** {value}\n"
                            )
                        case builtins.list:
                            creature_description += f"**{field.get('name')}:** "
                            for item in value:
                                creature_description += f"{item}, "
                            creature_description = creature_description[:-2] + "\n"
                embed.add_field(
                    name=creature.get("nome"),
                    value=creature_description,
                    inline=True,
                )
            embed.add_field(name="", value="", inline=False)

        for field in INLINE_FIELDS:
            value = self.match_values.get(field.get("key"))
            if value:
                embed.add_field(name=field.get("name"), value=value, inline=True)

        embed.set_footer(
            text=f'{self.match_values.get("livro")}, Página {self.match_values.get("pagina")}',
            icon_url=None,
        )

        return embed

    def _create_sugestions_embed(self) -> discord.Embed:
        title = "Magia não encontrada"
        description = "Não foi possível encontrar a magia desejada. \
            Abaixo estão algumas outras magias similares que podem ser do seu interesse.\n\
            Caso encontre a desejada, apenas clique no botão correspondente."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed

    def _create_none_sugestions_embed(self) -> discord.Embed:
        title = "Magia não encontrada"
        description = "Não foi possível encontrar a magia desejada ou qualquer outra semelhante.\n\
            Por favor, digite corretamente o nome da magia."

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed
