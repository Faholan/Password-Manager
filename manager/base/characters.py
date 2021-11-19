"""Define the characters used for generating passwords."""

from . import classes


BASE = classes.CharacterRange(
    "Letters",
    set(range(0x41, 0x5B)) | set(range(0x61, 0x7B)),
)

DIGITS = classes.CharacterRange("Digits", range(0x30, 0x40))
BASIC_SYMBOLS = classes.CharacterRange(
    "Basic symbols",
    set(range(0x20, 0x30))
    | set(range(0x3A, 0x41))
    | set(range(0x5B, 0x61))
    | set(range(0x7B, 0x7F)),
)

ADVANCED_SYMBOLS = classes.CharacterRange(
    "Advanced Symbols", set(range(0xA1, 0xBF)).difference({0xAD})
)

BASIC_ACCENTS = classes.CharacterRange(
    "Basic accents",
    set(range(0xC0, 0xFD)).difference(
        {
            0xC5,
            0xD0,
            0xD7,
            0xD8,
            0xDD,
            0xDE,
            0xE5,
            0xF0,
            0xF7,
            0xF8,
        }
    ),
)

ADVANCED_ACCENTS = classes.CharacterRange(
    "Advanced accents",
    {
        0xC5,
        0xD0,
        0xD8,
        0xE5,
        0xF0,
        0xF8,
        0xFD,
    }
    | set(range(0xFF, 0x17F)),
)

WEIRD_LETTERS = classes.CharacterRange(
    "Weird letters",
    set(range(0x17F, 0x2AF)),
)

GREEK = classes.CharacterRange(
    "Greek letters",
    set(range(0x391, 0x3AA)) | set(range(0x3B1, 0x3C9)),
)

COPTIC = classes.CharacterRange("Coptic letters", range(0x3E2, 0x3EF))

CYRILLIC = classes.CharacterRange("Cyrillic letters", range(0x410, 0x450))

CYRILLIC_WEIRD = classes.CharacterRange(
    "Weird cyrillic symbols",
    range(0x450, 0x52F),
)

ARMENIAN = classes.CharacterRange("Armenian letters", range(0x531, 0x587))

WEIRD_SYMBOLS = classes.CharacterRange("Weird symbols", range(0x2384, 0x23FB))

MORE_DIGITS = classes.CharacterRange(
    "More digits",
    set(range(0x2460, 0x249C)) | set(range(0x24EA, 0x2500)),
)

MORE_LETTERS = classes.CharacterRange("More letters", range(0x249C, 0x24EA))

BOXES = classes.CharacterRange("Boxes", range(0x2500, 0x2580))


ALL = (
    DIGITS,
    BASIC_SYMBOLS,
    ADVANCED_SYMBOLS,
    BASIC_ACCENTS,
    ADVANCED_ACCENTS,
    WEIRD_LETTERS,
    GREEK,
    COPTIC,
    CYRILLIC,
    CYRILLIC_WEIRD,
    ARMENIAN,
    WEIRD_SYMBOLS,
    MORE_DIGITS,
    MORE_LETTERS,
    BOXES,
)

REV_ALL = {charrange.name: i for i, charrange in enumerate(ALL)}
