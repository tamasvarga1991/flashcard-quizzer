"""Command-line entry point for the Flashcard Quizzer."""

import argparse
import sys
from collections.abc import Sequence

from utils.file_handler import FlashcardLoadError, load_flashcards
from utils.quiz_mode_factory import create_quiz_mode
from utils.quiz_modes import QuizEngine

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Study a flashcard deck in the selected quiz mode."
    )
    parser.add_argument(
        "-f", "--file", required=True, help="Path to a flashcard JSON file."
    )
    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        choices=("sequential", "random", "adaptive"),
        help="Quiz mode to use.",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display session statistics when the quiz ends.",
    )
    return parser


def display_statistics(
    total_questions: int,
    correct_answers: int,
    missed_terms: list[str],
) -> None:
    """Print the totals, accuracy, and unique missed front terms."""
    accuracy = correct_answers / total_questions * 100 if total_questions else 0.0
    missed_display = ", ".join(missed_terms) if missed_terms else "None"
    print("\nSession Statistics")
    print(f"Total Questions: {total_questions}")
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"Terms Missed: {missed_display}")


def run_quiz(engine: QuizEngine, show_stats: bool) -> None:
    """Run a quiz and optionally display partial or final statistics."""
    total_questions = 0
    correct_answers = 0
    missed_terms: list[str] = []
    missed_term_set: set[str] = set()

    try:
        while (selection := engine.next_card()) is not None:
            card_index, card = selection
            print(f"\n{card['front']}")
            answer = input("Your answer (or type 'exit' to stop): ")

            if answer.strip().casefold() == "exit":
                print("Quiz stopped.")
                break

            is_correct = answer.strip().casefold() == card["back"].strip().casefold()
            total_questions += 1
            if is_correct:
                correct_answers += 1
                print(f"{GREEN}Correct!{RESET}")
            else:
                print(f"{RED}Incorrect. Correct answer: {card['back']}{RESET}")
                front = card["front"]
                if front not in missed_term_set:
                    missed_term_set.add(front)
                    missed_terms.append(front)

            engine.record_answer(card_index, is_correct)
    except KeyboardInterrupt:
        print("\nQuiz interrupted.")

    if show_stats:
        display_statistics(total_questions, correct_answers, missed_terms)


def main(argv: Sequence[str] | None = None) -> int:
    """Parse CLI arguments, load a deck, and run a quiz session."""
    args = build_parser().parse_args(argv)

    try:
        cards = load_flashcards(args.file)
    except FlashcardLoadError as error:
        print(f"Error loading flashcards: {error}", file=sys.stderr)
        return 1

    mode = create_quiz_mode(args.mode, cards)
    engine = QuizEngine(mode)
    if not cards:
        print("No flashcards available.")
        if args.stats:
            display_statistics(0, 0, [])
        return 0

    run_quiz(engine, args.stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
