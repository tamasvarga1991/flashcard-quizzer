"""Quiz scheduling strategies and a small engine that delegates to them."""

import random
from abc import ABC, abstractmethod
from collections import deque
from typing import Any

Flashcard = dict[str, Any]
CardSelection = tuple[int, Flashcard]


class QuizMode(ABC):
    """Abstract strategy for selecting cards during a quiz."""

    def __init__(self, cards: list[Flashcard]) -> None:
        """Keep the cards while leaving the caller's list untouched."""
        self._cards = list(cards)

    @abstractmethod
    def next_card(self) -> CardSelection | None:
        """Return the next original index and card, or ``None`` when done."""

    def record_answer(self, card_index: int, is_correct: bool) -> None:
        """Receive answer feedback; non-adaptive modes do not use it."""


class SequentialMode(QuizMode):
    """Serve each card once in its original order."""

    def __init__(self, cards: list[Flashcard]) -> None:
        super().__init__(cards)
        self._next_index = 0

    def next_card(self) -> CardSelection | None:
        if self._next_index >= len(self._cards):
            return None

        card_index = self._next_index
        self._next_index += 1
        return card_index, self._cards[card_index]


class RandomMode(QuizMode):
    """Serve each card once in a shuffled order."""

    def __init__(self, cards: list[Flashcard]) -> None:
        super().__init__(cards)
        self._order = list(range(len(self._cards)))
        random.shuffle(self._order)
        self._next_position = 0

    def next_card(self) -> CardSelection | None:
        if self._next_position >= len(self._order):
            return None

        card_index = self._order[self._next_position]
        self._next_position += 1
        return card_index, self._cards[card_index]


class AdaptiveMode(QuizMode):
    """Prioritize missed cards until they are eventually answered correctly."""

    def __init__(self, cards: list[Flashcard]) -> None:
        super().__init__(cards)
        self._pending_indices = deque(range(len(self._cards)))
        self._current_index: int | None = None

    def next_card(self) -> CardSelection | None:
        if self._current_index is not None:
            raise RuntimeError(
                "Record the current card's answer before continuing."
            )
        if not self._pending_indices:
            return None

        card_index = self._pending_indices.popleft()
        self._current_index = card_index
        return card_index, self._cards[card_index]

    def record_answer(self, card_index: int, is_correct: bool) -> None:
        """Requeue an incorrect card at the front until answered correctly."""
        if card_index != self._current_index:
            raise ValueError(
                "The answer must match the currently served card."
            )

        if not is_correct:
            self._pending_indices.appendleft(card_index)
        self._current_index = None


class QuizEngine:
    """Delegate card selection and answer feedback to a quiz mode."""

    def __init__(self, mode: QuizMode) -> None:
        """Create an engine using the selected scheduling strategy."""
        self._mode = mode

    def next_card(self) -> CardSelection | None:
        """Return the next card selection from the configured mode."""
        return self._mode.next_card()

    def record_answer(self, card_index: int, is_correct: bool) -> None:
        """Pass answer feedback to the configured mode."""
        self._mode.record_answer(card_index, is_correct)
