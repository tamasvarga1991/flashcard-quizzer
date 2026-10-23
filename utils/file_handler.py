"""Load and validate flashcard decks stored as JSON."""

import json
from pathlib import Path
from typing import Any


class FlashcardLoadError(Exception):
    """Raised when a flashcard deck cannot be read or validated."""


def load_flashcards(path: str | Path) -> list[dict[str, Any]]:
    """Load flashcards from an array or an object containing a ``cards`` array.

    Each card must be an object with string-valued ``front`` and ``back``
    fields. Additional card fields are preserved.

    Args:
        path: Path to the JSON file containing the deck.

    Returns:
        The validated list of flashcard objects.

    Raises:
        FlashcardLoadError: If the file cannot be read, its JSON is malformed,
            or its contents do not match a supported flashcard structure.
    """
    deck_path = Path(path)
    try:
        with deck_path.open(encoding="utf-8") as deck_file:
            data: Any = json.load(deck_file)
    except FileNotFoundError:
        raise FlashcardLoadError(f"Flashcard file not found: {deck_path}") from None
    except OSError:
        raise FlashcardLoadError(
            f"Could not read flashcard file: {deck_path}"
        ) from None
    except UnicodeDecodeError:
        raise FlashcardLoadError(
            f"Flashcard file is not valid UTF-8: {deck_path}"
        ) from None
    except json.JSONDecodeError as error:
        raise FlashcardLoadError(
            f"Invalid JSON in flashcard file {deck_path} "
            f"at line {error.lineno}, column {error.colno}"
        ) from None

    if isinstance(data, dict):
        cards = data.get("cards")
        if not isinstance(cards, list):
            raise FlashcardLoadError(
                "Flashcard data object must contain a " "'cards' array."
            )
    elif isinstance(data, list):
        cards = data
    else:
        raise FlashcardLoadError(
            "Flashcard data must be an array or an object containing a "
            "'cards' array."
        )

    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            raise FlashcardLoadError(f"Card at index {index} must be an object.")

        for field in ("front", "back"):
            if field not in card:
                raise FlashcardLoadError(
                    f"Card at index {index} is missing required " f"field '{field}'."
                )
            if not isinstance(card[field], str):
                raise FlashcardLoadError(
                    f"Card at index {index} field '{field}' must be a string."
                )

    return cards
