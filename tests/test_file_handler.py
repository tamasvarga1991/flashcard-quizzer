"""Tests for loading and validating flashcard JSON files."""

import json
from pathlib import Path

import pytest

from utils.file_handler import FlashcardLoadError, load_flashcards


def write_json(path: Path, data: object) -> None:
    """Write JSON test data to a temporary file."""
    path.write_text(json.dumps(data), encoding="utf-8")


def test_load_flashcards_from_top_level_array(tmp_path: Path) -> None:
    """Load valid cards when the JSON root is an array."""
    expected = [
        {"front": "API", "back": "Application Programming Interface"},
        {"front": "CPU", "back": "Central Processing Unit"},
    ]
    deck_path = tmp_path / "array_deck.json"
    write_json(deck_path, expected)

    assert load_flashcards(deck_path) == expected


def test_load_flashcards_from_cards_object(tmp_path: Path) -> None:
    """Load valid cards when they are nested under the cards key."""
    expected = [{"front": "Keyword", "back": "def"}]
    deck_path = tmp_path / "object_deck.json"
    write_json(deck_path, {"cards": expected})

    assert load_flashcards(deck_path) == expected


@pytest.mark.parametrize("data", [[], {"cards": []}])
def test_load_flashcards_allows_empty_decks(
    tmp_path: Path, data: object
) -> None:
    """Accept empty arrays in either supported format."""
    deck_path = tmp_path / "empty_deck.json"
    write_json(deck_path, data)

    assert load_flashcards(deck_path) == []


def test_load_flashcards_allows_empty_front_and_back(tmp_path: Path) -> None:
    """Accept empty strings for required card fields."""
    deck_path = tmp_path / "empty_strings.json"
    write_json(deck_path, [{"front": "", "back": ""}])

    assert load_flashcards(deck_path) == [{"front": "", "back": ""}]


def test_load_flashcards_preserves_additional_card_fields(
    tmp_path: Path,
) -> None:
    """Keep extra fields on validated card objects."""
    expected = [{"front": "Question", "back": "Answer", "tag": ["topic"]}]
    deck_path = tmp_path / "extra_fields.json"
    write_json(deck_path, expected)

    assert load_flashcards(deck_path) == expected


def test_load_flashcards_rejects_malformed_json(tmp_path: Path) -> None:
    """Report malformed JSON as an application-specific error."""
    deck_path = tmp_path / "malformed.json"
    deck_path.write_text("[{not valid json]", encoding="utf-8")

    with pytest.raises(FlashcardLoadError, match="Invalid JSON"):
        load_flashcards(deck_path)


def test_load_flashcards_rejects_invalid_utf8(tmp_path: Path) -> None:
    """Report invalid UTF-8 as an application-specific error."""
    deck_path = tmp_path / "invalid_encoding.json"
    deck_path.write_bytes(b"\xff\xfe\xfa")

    with pytest.raises(FlashcardLoadError, match="not valid UTF-8"):
        load_flashcards(deck_path)


def test_load_flashcards_rejects_missing_file(tmp_path: Path) -> None:
    """Report a missing file as an application-specific error."""
    with pytest.raises(FlashcardLoadError, match="file not found"):
        load_flashcards(tmp_path / "missing.json")


def test_load_flashcards_rejects_unreadable_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Report file I/O errors without leaking the underlying exception."""
    deck_path = tmp_path / "unreadable.json"

    def raise_permission_error(*args: object, **kwargs: object) -> None:
        raise PermissionError("permission denied")

    monkeypatch.setattr(Path, "open", raise_permission_error)

    with pytest.raises(
        FlashcardLoadError, match="Could not read flashcard file"
    ):
        load_flashcards(deck_path)


@pytest.mark.parametrize("data", [None, "cards", 42, True])
def test_load_flashcards_rejects_invalid_top_level_values(
    tmp_path: Path, data: object
) -> None:
    """Reject JSON roots that are neither supported format."""
    deck_path = tmp_path / "invalid_root.json"
    write_json(deck_path, data)

    with pytest.raises(FlashcardLoadError, match="Flashcard data must be"):
        load_flashcards(deck_path)


@pytest.mark.parametrize(
    "data", [{}, {"other": []}, {"cards": None}, {"cards": {}}]
)
def test_load_flashcards_rejects_missing_or_invalid_cards_array(
    tmp_path: Path, data: object
) -> None:
    """Require an object-format deck to contain a cards array."""
    deck_path = tmp_path / "missing_cards.json"
    write_json(deck_path, data)

    with pytest.raises(
        FlashcardLoadError, match="must contain a 'cards' array"
    ):
        load_flashcards(deck_path)


def test_load_flashcards_rejects_non_object_card(tmp_path: Path) -> None:
    """Reject entries that are not card objects."""
    deck_path = tmp_path / "invalid_card.json"
    write_json(deck_path, ["not a card"])

    with pytest.raises(
        FlashcardLoadError, match="Card at index 0 must be an object"
    ):
        load_flashcards(deck_path)


@pytest.mark.parametrize(
    ("card", "missing_field"),
    [({"back": "Answer"}, "front"), ({"front": "Question"}, "back")],
)
def test_load_flashcards_rejects_missing_required_field(
    tmp_path: Path, card: dict[str, str], missing_field: str
) -> None:
    """Reject cards missing either required field."""
    deck_path = tmp_path / "missing_field.json"
    write_json(deck_path, [card])

    with pytest.raises(
        FlashcardLoadError,
        match=f"missing required field '{missing_field}'",
    ):
        load_flashcards(deck_path)


@pytest.mark.parametrize(
    ("card", "invalid_field"),
    [
        ({"front": 1, "back": "Answer"}, "front"),
        ({"front": "Question", "back": None}, "back"),
    ],
)
def test_load_flashcards_rejects_non_string_field(
    tmp_path: Path, card: dict[str, object], invalid_field: str
) -> None:
    """Require both required field values to be strings."""
    deck_path = tmp_path / "invalid_field.json"
    write_json(deck_path, [card])

    with pytest.raises(
        FlashcardLoadError,
        match=f"field '{invalid_field}' must be a string",
    ):
        load_flashcards(deck_path)
