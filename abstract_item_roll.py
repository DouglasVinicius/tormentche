import discord

from abc import ABC, abstractmethod
from dice_roll import DiceRoll


class AbstractItemRoll(ABC):
    def __init__(self, json_data: dict) -> None:
        self.dice_roll = DiceRoll()
        self.json_data = json_data

    def make_roll(self, number_of_rolls: int = 1) -> list[dict]:
        items = self._get_items()
        if not number_of_rolls or number_of_rolls < 1:
            number_of_rolls = 1

        rolled_items = []
        for _ in range(number_of_rolls):
            _, _, roll = self.dice_roll.make_roll("1d100")
            rolled_item = next(
                item
                for item in items
                if roll >= item.get("porcentagem").get("inicio")
                and roll <= item.get("porcentagem").get("fim")
            )
            rolled_items.append(
                {
                    "item": rolled_item,
                    "roll": roll,
                }
            )

        return rolled_items

    @abstractmethod
    def _get_items(self) -> list[dict]:
        pass

    @abstractmethod
    def create_embeds(
        self, rolled_items: list[dict]
    ) -> list[discord.Embed] | discord.Embed:
        pass
