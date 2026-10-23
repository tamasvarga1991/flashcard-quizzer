"""Factory for creating flashcard quiz scheduling strategies."""

from utils.quiz_modes import (
    AdaptiveMode,
    Flashcard,
    QuizMode,
    RandomMode,
    SequentialMode,
)


def create_quiz_mode(mode_name: str, cards: list[Flashcard]) -> QuizMode:
    """Create a supported quiz mode for the supplied cards.

    Args:
        mode_name: One of ``sequential``, ``random``, or ``adaptive``.
        cards: Flashcards to schedule.

    Returns:
        A new quiz mode instance.

    Raises:
        ValueError: If ``mode_name`` is not a supported mode.
    """
    mode_types: dict[str, type[QuizMode]] = {
        "sequential": SequentialMode,
        "random": RandomMode,
        "adaptive": AdaptiveMode,
    }
    try:
        mode_type = mode_types[mode_name]
    except KeyError:
        raise ValueError(f"Unsupported quiz mode: {mode_name}") from None
    return mode_type(cards)
