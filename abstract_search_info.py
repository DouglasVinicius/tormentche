import builtins
import discord

from difflib import SequenceMatcher
from itertools import islice
from abc import ABC, abstractmethod
from utils.utils import name_normalizer


MAX_SUGGESTION_ITEMS = 5
SIMILARITY_FLOOR_VALUE = 0.6


class AbstractSearchInfo(ABC):
    def __init__(self, json_data: list[dict]) -> None:
        self.json_data = json_data

    def get_correct_match(self, input: str) -> dict | list[dict]:
        normalized_input = name_normalizer(input)
        match_result = self._get_exact_match(normalized_input)
        if not match_result:
            match_result = self._get_included_matches(normalized_input)
            if not (len(match_result) > 0):
                match_result = self._get_top_similarities(normalized_input)
        return match_result

    def _get_exact_match(self, normalized_input: str) -> dict | None:
        return next(
            (
                item
                for item in self.json_data
                if item.get("normalized_name") == normalized_input
            ),
            None,
        )

    def _get_included_matches(self, normalized_input: str) -> list:
        top_items = list(
            islice(
                (
                    value
                    for value in self.json_data
                    if value.get("normalized_name").find(normalized_input) >= 0
                ),
                MAX_SUGGESTION_ITEMS,
            )
        )
        return top_items

    def _get_top_similarities(self, normalized_input: str) -> list:
        top_similarities = list()
        for value in self.json_data:
            similarity = SequenceMatcher(
                None,
                normalized_input,
                value.get("normalized_name"),
            ).ratio()
            similarity_object = {
                "similarity": similarity,
                "value": value,
            }

            if similarity > SIMILARITY_FLOOR_VALUE:
                if len(top_similarities) < MAX_SUGGESTION_ITEMS:
                    top_similarities.append(similarity_object)
                else:
                    if similarity > top_similarities[-1].get("similarity"):
                        top_similarities.pop()
                        top_similarities.append(similarity_object)
            top_similarities.sort(key=lambda item: item.get("similarity"), reverse=True)
        return [similarity.get("value") for similarity in top_similarities]

    @abstractmethod
    def create_embeds(
        self, match_values: dict | list[dict]
    ) -> list[discord.Embed] | discord.Embed:
        self.match_values = match_values
        return self._create_description_embed()

    def _create_description_embed(self) -> discord.Embed:
        match type(self.match_values):
            case builtins.dict:
                return self._create_exact_embed()
            case builtins.list:
                if len(self.match_values) > 0:
                    return self._create_sugestions_embed()
                else:
                    return self._create_none_sugestions_embed()

    @abstractmethod
    def _create_exact_embed(self) -> discord.Embed:
        pass

    @abstractmethod
    def _create_sugestions_embed(self) -> discord.Embed:
        pass

    @abstractmethod
    def _create_none_sugestions_embed(self) -> discord.Embed:
        pass
