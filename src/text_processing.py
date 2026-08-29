"""Small, deterministic text-processing helpers."""

import re


def clean_ocr_text(text: str) -> str:
    """Remove repeated whitespace while retaining paragraph breaks."""
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    paragraphs = []
    current = []
    for line in lines:
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)


_BRAILLE = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋",
    "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚", "k": "⠅", "l": "⠇",
    "m": "⠍", "n": "⠝", "o": "⠕", "p": "⠏", "q": "⠟", "r": "⠗",
    "s": "⠎", "t": "⠞", "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭",
    "y": "⠽", "z": "⠵", " ": " ", ",": "⠂", ".": "⠲", "?": "⠦",
    "!": "⠖", "-": "⠤", "\n": "\n",
}


def text_to_braille(text: str) -> str:
    """Convert Latin letters and basic punctuation to Grade 1 Unicode Braille."""
    return "".join(_BRAILLE.get(character.lower(), character) for character in text)
