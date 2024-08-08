import discord
import datetime
import builtins


class CustomEmbed:
    def __init__(self, selected_values: dict | list[dict], embed_type: str) -> None:
        self.selected_values = selected_values
        self.embed_type = embed_type

    def create_related_items_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="Condições relacionadas",
            description="As seguintes condições tem relação com a condição encontrada. \
                Caso queira visualizá-las também, clique no respectivo botão.",
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        return embed

    def create_description_embed(self) -> discord.Embed:
        match type(self.selected_values):
            case builtins.dict:
                return self.__create_exact_embed()
            case builtins.list:
                if len(self.selected_values) > 0:
                    return self.__create_similarity_embed()
                else:
                    return self.__create_none_similarity_embed()

    def __create_exact_embed(self) -> discord.Embed:
        INLINE_FIELDS = [
            {"key": "resistencia", "name": "Resistência"},
            {"key": "alvo", "name": "Alvo"},
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
            title=self.selected_values.get("nome"),
            description=self.selected_values.get("descricao"),
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        match self.embed_type:
            case "magic":
                upgrades = self.selected_values.get("aprimoramentos")
                if upgrades:
                    for upgrade in upgrades:
                        embed.add_field(
                            name=upgrade.get("custo"),
                            value=upgrade.get("descricao"),
                            inline=False,
                        )

                classification = self.selected_values.get("classificacao")
                circle = self.selected_values.get("circulo")
                school = self.selected_values.get("escola")
                if classification and circle and school:
                    embed.set_author(
                        name=f"{classification} {circle}, {school}",
                        url=None,
                        icon_url=None,
                    )

                creatures = self.selected_values.get("criaturas")
                if creatures:
                    embed.add_field(
                        name="\nEstatística das Criaturas", value="", inline=False
                    )
                    for creature in creatures:
                        creatures_description = ""
                        for field in CREATURES_FIELDS:
                            field_value = creature.get(field.get("key"))
                            match type(field_value):
                                case builtins.str | builtins.int:
                                    creatures_description += (
                                        f"**{field.get('name')}:** {field_value}\n"
                                    )
                                case builtins.list:
                                    creatures_description += (
                                        f"**{field.get('name')}:** "
                                    )
                                    for item in field_value:
                                        creatures_description += f"{item}, "
                                    creatures_description = (
                                        creatures_description[:-2] + "\n"
                                    )
                        embed.add_field(
                            name=creature.get("nome"),
                            value=creatures_description,
                            inline=True,
                        )
                    embed.add_field(name="", value="", inline=False)

            case "status":
                status_type = self.selected_values.get("tipo")
                if status_type:
                    embed.add_field(name="Tipo", value=status_type, inline=False)

        for value in INLINE_FIELDS:
            field_value = self.selected_values.get(value.get("key"))
            if field_value:
                embed.add_field(name=value.get("name"), value=field_value, inline=True)

        embed.set_footer(
            text=f'{self.selected_values.get("livro")}, Página {self.selected_values.get("pagina")}',
            icon_url=None,
        )

        return embed

    def __create_similarity_embed(self) -> discord.Embed:
        match self.embed_type:
            case "magic":
                title = "Magia não encontrada"
                description = "Não foi possível encontrar a magia desejada. \
                    Abaixo estão algumas outras magias similares que podem ser do seu interesse.\n\
                    Caso encontre a desejada, apenas clique no botão correspondente."
            case "status":
                title = "Condição não encontrada"
                description = "Não foi possível encontrar a condição desejada. \
                    Abaixo estão algumas outras condições similares que podem ser do seu interesse.\n\
                    Caso encontre a desejada, apenas clique no botão correspondente."
            case "maneuver":
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

    def __create_none_similarity_embed(self) -> discord.Embed:
        match self.embed_type:
            case "magic":
                title = "Magia não encontrada"
                description = "Não foi possível encontrar a magia desejada ou qualquer outra semelhante.\n\
                    Por favor, digite corretamente o nome da magia."
            case "status":
                title = "Condição não encontrada"
                description = "Não foi possível encontrar a condição desejada ou qualquer outra semelhante.\n\
                    Por favor, digite corretamente o nome da condição."
            case "maneuver":
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
