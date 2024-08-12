import re
import random
import math


class DiceRoll:
    ACCEPTED_CHARACTERS = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "d",
        "+",
        "-",
        "*",
        "/",
    ]

    def __normalize_roll(self, roll: str) -> str:
        cleaned_roll = "".join(
            char for char in roll if char in self.ACCEPTED_CHARACTERS
        )
        normalized_roll = re.sub(r"(d)+", "d", cleaned_roll)
        return normalized_roll

    def __roll_dice(self, dices: str) -> list[int]:
        number_of_dices, dice_sides = map(int, dices.split("d"))
        return [random.randint(1, dice_sides) for _ in range(number_of_dices)]

    def __replace_dice_with_rolled_value(self, match) -> str:
        dice_result = self.__roll_dice(match.group())
        dice_result_str = "".join(f"{result}+" for result in dice_result)
        dice_result_str = dice_result_str[:-1]
        return f"({dice_result_str})"

    def make_roll(self, roll: str) -> tuple[str, str, int]:
        normalized_roll = self.__normalize_roll(roll)
        dice_pattern = re.compile(r"(\d+d\d+)")

        math_expression = dice_pattern.sub(
            self.__replace_dice_with_rolled_value, normalized_roll
        )
        return normalized_roll, math_expression, math.floor(eval(math_expression))
