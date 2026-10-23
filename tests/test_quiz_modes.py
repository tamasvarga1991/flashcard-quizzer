"""Tests for quiz scheduling strategies and their factory."""

from copy import deepcopy

import pytest

from utils.quiz_mode_factory import create_quiz_mode
from utils.quiz_modes import AdaptiveMode, QuizEngine, RandomMode, SequentialMode


def make_cards() -> list[dict[str, str]]:
    """Return a small distinct deck for mode tests."""
    return [
        {"front": "First", "back": "1"},
        {"front": "Second", "back": "2"},
        {"front": "Third", "back": "3"},
    ]


def test_sequential_mode_serves_cards_in_original_order() -> None:
    """Return each card once, in its original position order."""
    cards = make_cards()
    mode = SequentialMode(cards)

    assert [mode.next_card() for _ in cards] == list(enumerate(cards))
    assert mode.next_card() is None


def test_random_mode_shuffles_a_copy_and_serves_every_card_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Serve shuffled original positions without changing the input list."""
    cards = make_cards()
    original_cards = deepcopy(cards)
    monkeypatch.setattr(
        "utils.quiz_modes.random.shuffle",
        lambda positions: positions.reverse(),
    )
    mode = RandomMode(cards)

    selections = [mode.next_card() for _ in cards]

    assert selections == [(2, cards[2]), (1, cards[1]), (0, cards[0])]
    assert cards == original_cards
    assert mode.next_card() is None


def test_adaptive_mode_requires_answer_before_next_card() -> None:
    """Reject advancing while a served card is awaiting an answer."""
    cards = make_cards()
    mode = AdaptiveMode(cards)

    assert mode.next_card() == (0, cards[0])
    with pytest.raises(
        RuntimeError,
        match="current card's answer",
    ):
        mode.next_card()

    mode.record_answer(0, True)
    assert mode.next_card() == (1, cards[1])


def test_adaptive_mode_rejects_answer_for_wrong_card_index() -> None:
    """Reject feedback for an index other than the currently served card."""
    cards = make_cards()
    mode = AdaptiveMode(cards)

    assert mode.next_card() == (0, cards[0])
    with pytest.raises(ValueError, match="currently served card"):
        mode.record_answer(1, True)

    mode.record_answer(0, True)
    assert mode.next_card() == (1, cards[1])


def test_adaptive_mode_rejects_duplicate_answer_submission() -> None:
    """Reject a second answer for the same served card."""
    cards = make_cards()
    mode = AdaptiveMode(cards)

    assert mode.next_card() == (0, cards[0])
    mode.record_answer(0, True)
    with pytest.raises(ValueError, match="currently served card"):
        mode.record_answer(0, True)

    assert mode.next_card() == (1, cards[1])


def test_adaptive_mode_behavior() -> None:
    """Repeated misses stay prioritized until answered correctly."""
    cards = make_cards()
    engine = QuizEngine(AdaptiveMode(cards))

    assert engine.next_card() == (0, cards[0])
    engine.record_answer(0, False)
    assert engine.next_card() == (0, cards[0])
    engine.record_answer(0, False)
    assert engine.next_card() == (0, cards[0])
    engine.record_answer(0, True)

    assert engine.next_card() == (1, cards[1])


def test_adaptive_mode_tracks_identical_cards_by_position() -> None:
    """Identical card contents remain separate scheduled cards."""
    first_card = {"front": "Same", "back": "Answer"}
    second_card = {"front": "Same", "back": "Answer"}
    mode = AdaptiveMode([first_card, second_card])

    assert mode.next_card() == (0, first_card)
    mode.record_answer(0, False)
    assert mode.next_card() == (0, first_card)
    mode.record_answer(0, True)
    assert mode.next_card() == (1, second_card)


@pytest.mark.parametrize(
    ("mode_name", "expected_type"),
    [
        ("sequential", SequentialMode),
        ("random", RandomMode),
        ("adaptive", AdaptiveMode),
    ],
)
def test_quiz_mode_factory(
    mode_name: str,
    expected_type: type[SequentialMode | RandomMode | AdaptiveMode],
) -> None:
    """Create each supported quiz strategy from its mode name."""
    assert isinstance(create_quiz_mode(mode_name, make_cards()), expected_type)


def test_quiz_mode_factory_rejects_unsupported_mode() -> None:
    """Raise a clear error when a mode name is unsupported."""
    with pytest.raises(ValueError, match="Unsupported quiz mode: typing"):
        create_quiz_mode("typing", make_cards())


@pytest.mark.parametrize("mode_type", [SequentialMode, RandomMode, AdaptiveMode])
def test_quiz_modes_return_none_for_empty_decks(
    mode_type: type[SequentialMode | RandomMode | AdaptiveMode],
) -> None:
    """All modes report completion immediately for an empty deck."""
    assert mode_type([]).next_card() is None
