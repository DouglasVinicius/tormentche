import discord
import datetime


class DiceRollEmbed:
    def create_dice_roll_embed(
        self, entry_expression: str, resolved_expression: str, roll_result: int
    ) -> discord.Embed:
        dice_roll_embed = discord.Embed(
            title="Expressão recebida",
            description=entry_expression,
            color=discord.Colour.brand_red(),
            timestamp=datetime.datetime.now(),
        )

        dice_roll_embed.add_field(
            name="Resultado das rolagens",
            value=resolved_expression,
            inline=False,
        )
        dice_roll_embed.add_field(
            name="Valor final",
            value=roll_result,
            inline=False,
        )

        return dice_roll_embed
