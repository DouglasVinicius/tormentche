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


def name_normalizer(word: str) -> str:
    formated_word = word.lower()
    for remove_char in SHOULD_REMOVE_CHARACTERS:
        formated_word = formated_word.replace(remove_char, "")
    return unidecode(formated_word)
