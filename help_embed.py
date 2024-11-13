import discord
import datetime


class HelpEmbed:
    def create_help_embed(self) -> discord.Embed:
        help_embed = discord.Embed(
            title="Comandos disponíveis",
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        help_embed.add_field(
            name="/magias",
            value="Procura e exibe a descrição detalhada da magia especificada. Informe o nome da magia que deseja consultar.",
            inline=False,
        )
        help_embed.add_field(
            name="/condicoes",
            value="Procura e exibe a descrição da condição informada. Digite o nome da condição para obter suas informações. Caso a condição procurada tenha relação com outras condições em seu texto, as retorná em botões que exibirão suas descrições ao clique.",
            inline=False,
        )
        help_embed.add_field(
            name="/manobras",
            value="Procura e exibe a descrição da manobra de combate indicada. Informe o nome da manobra para ver os detalhes.",
            inline=False,
        )
        help_embed.add_field(
            name="/parceiros",
            value="Procura e exibe a descrição do parceiro mencionado. Digite o nome do parceiro para obter a descrição correspondente.",
            inline=False,
        )
        help_embed.add_field(
            name="/rolar",
            value="Rola dados e calcula o resultado de expressões matemáticas. Use a sintaxe 'XdY', onde 'X' é o número de dados e 'Y' o número de faces. Você pode combinar múltiplos lançamentos e operações matemáticas.",
            inline=False,
        )
        help_embed.add_field(
            name="/pocoes",
            value="Rola um número X de poções utilizando a tabela de poções. Por padrão, caso o numero desejado de poções passado seja menor que 1, 1 poção é rolada.",
            inline=False,
        )

        return help_embed
