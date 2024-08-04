from difflib import SequenceMatcher
from unidecode import unidecode


SHOULD_REMOVE_CHARACTERS = [
    " ",
    "'",
    '"',
    "!",
    "@",
    "#",
    "$",
    "%",
    "¨",
    "&",
    "*",
    "(",
    ")",
    "-",
    "_",
    "=",
    "+",
    "`",
    "´",
    "[",
    "]",
    "{",
    "}",
    "~",
    "^",
    "/",
    "?",
    ";",
    ":",
    ".",
    ">",
    ",",
    "<",
    "\\",
    "|",
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
]
MAX_SUGGESTION_ITEMS = 5
FLOOR_SIMILARITY_VALUE = 0.6


def normalize_names(word: str) -> str:
    formated_word = word.lower()
    for remove_char in SHOULD_REMOVE_CHARACTERS:
        formated_word = formated_word.replace(remove_char, "")
    return unidecode(formated_word)


def json_names_normalization(related_json: list[dict]) -> list:
    for item in related_json:
        item["normalized_name"] = normalize_names(item.get("nome"))
    return related_json


def get_exact_match(related_json: list[dict], input: str) -> dict | None:
    normalized_input = normalize_names(input)
    for item in related_json:
        if item.get("normalized_name") == normalized_input:
            return item


def get_included_matches(related_json: list[dict], input: str) -> list:
    top = []
    normalized_input = normalize_names(input)
    for index, value in enumerate(related_json):
        if value.get("normalized_name").find(normalized_input) >= 0:
            top.append(index)
            if len(top) >= MAX_SUGGESTION_ITEMS:
                return [related_json[index] for index in top]
    return [related_json[index] for index in top]


def get_top_similarities(related_json: list[dict], input: str) -> list:
    top = []
    normalized_input = normalize_names(input)
    for index, value in enumerate(related_json):
        similarity = SequenceMatcher(
            None,
            normalized_input,
            value.get("normalized_name"),
        ).ratio()
        similarity_object = {
            "similarity": similarity,
            "index": index,
        }

        if similarity > FLOOR_SIMILARITY_VALUE:
            if len(top) < MAX_SUGGESTION_ITEMS:
                top.append(similarity_object)
            else:
                if similarity > top[-1].get("similarity"):
                    top.pop()
                    top.append(similarity_object)
        top.sort(key=lambda item: item.get("similarity"), reverse=True)
    return [related_json[item.get("index")] for item in top]
