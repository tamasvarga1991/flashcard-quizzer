"""Integration tests for the Flashcard Quizzer CLI."""

import json
from pathlib import Path

import pytest

from main import main


def write_deck(path: Path, cards: list[dict[str, str]]) -> None:
    """Write a temporary flashcard deck in JSON format."""
    path.write_text(json.dumps(cards), encoding="utf-8")


def test_full_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Run three questions and verify feedback and final statistics."""
    deck_path = tmp_path / "deck.json"
    write_deck(
        deck_path,
        [
            {"front": "Alpha", "back": "One"},
            {"front": "Beta", "back": "Two"},
            {"front": "Gamma", "back": "Three"},
        ],
    )
    answers = iter(["  oNe  ", "incorrect", "THREE"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    result = main(
        ["--file", str(deck_path), "--mode", "sequential", "--stats"]
    )

    output = capsys.readouterr().out
    assert result == 0
    assert "\033[32mCorrect!\033[0m" in output
    assert "\033[31mIncorrect. Correct answer: Two\033[0m" in output
    assert output.count("\033[32mCorrect!\033[0m") == 2
    assert "Total Questions: 3" in output
    assert "Accuracy: 66.7%" in output
    assert "Terms Missed: Beta" in output


@pytest.mark.parametrize("argv", [[], ["--file", "deck.json"]])
def test_cli_requires_file_and_mode(
    argv: list[str], capsys: pytest.CaptureFixture[str]
) -> None:
    """Require both deck path and quiz mode arguments."""
    with pytest.raises(SystemExit) as error:
        main(argv)

    assert error.value.code == 2
    assert "required" in capsys.readouterr().err


def test_cli_rejects_invalid_mode(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Let argparse reject a mode outside the supported choices."""
    with pytest.raises(SystemExit) as error:
        main(["--file", "deck.json", "--mode", "unsupported"])

    assert error.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_cli_help_displays_usage(capsys: pytest.CaptureFixture[str]) -> None:
    """Expose argparse's built-in help without loading a deck."""
    with pytest.raises(SystemExit) as error:
        main(["--help"])

    assert error.value.code == 0
    assert "usage:" in capsys.readouterr().out


def test_loader_error_is_reported_without_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Return a failure status and a concise error for a missing deck."""
    result = main(
        ["--file", str(tmp_path / "missing.json"), "--mode", "sequential"]
    )

    captured = capsys.readouterr()
    assert result == 1
    assert "Error loading flashcards: Flashcard file not found" in captured.err
    assert "Traceback" not in captured.err


def test_exit_stops_without_counting_current_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Show stats for answered attempts and exclude the exit prompt."""
    deck_path = tmp_path / "deck.json"
    write_deck(
        deck_path,
        [
            {"front": "Alpha", "back": "One"},
            {"front": "Beta", "back": "Two"},
            {"front": "Gamma", "back": "Three"},
        ],
    )
    answers = iter(["wrong", "  EXIT  "])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    result = main(
        ["--file", str(deck_path), "--mode", "sequential", "--stats"]
    )

    output = capsys.readouterr().out
    assert result == 0
    assert "Quiz stopped." in output
    assert output.count("Incorrect.") == 1
    assert "Total Questions: 1" in output
    assert "Accuracy: 0.0%" in output
    assert "Terms Missed: Alpha" in output


def test_ctrl_c_stops_gracefully_and_shows_partial_statistics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Catch Ctrl+C during input and report partial stats without traceback."""
    deck_path = tmp_path / "deck.json"
    write_deck(
        deck_path,
        [
            {"front": "Alpha", "back": "One"},
            {"front": "Beta", "back": "Two"},
        ],
    )
    answers = iter(["wrong"])

    def interrupt(_prompt: str) -> str:
        try:
            return next(answers)
        except StopIteration:
            raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", interrupt)

    result = main(
        ["--file", str(deck_path), "--mode", "sequential", "--stats"]
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Quiz interrupted." in captured.out
    assert "Traceback" not in captured.out
    assert "Traceback" not in captured.err
    assert "Total Questions: 1" in captured.out
    assert "Accuracy: 0.0%" in captured.out
    assert "Terms Missed: Alpha" in captured.out


def test_adaptive_session_counts_retries_and_unique_missed_terms(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Count repeated adaptive attempts while listing a missed term once."""
    deck_path = tmp_path / "adaptive_deck.json"
    write_deck(deck_path, [{"front": "Alpha", "back": "One"}])
    answers = iter(["wrong", "still wrong", "one"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))

    result = main(
        ["--file", str(deck_path), "--mode", "adaptive", "--stats"]
    )

    output = capsys.readouterr().out
    stats = output.split("Session Statistics", maxsplit=1)[1]
    assert result == 0
    assert output.count("\nAlpha\n") == 3
    assert output.count("\033[31mIncorrect.") == 2
    assert output.count("\033[32mCorrect!") == 1
    assert "Total Questions: 3" in stats
    assert "Accuracy: 33.3%" in stats
    assert stats.count("Alpha") == 1
    assert "Terms Missed: Alpha" in stats


def test_statistics_are_not_displayed_without_flag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Keep session statistics opt-in."""
    deck_path = tmp_path / "deck.json"
    write_deck(deck_path, [{"front": "Alpha", "back": "One"}])
    monkeypatch.setattr("builtins.input", lambda _prompt: "one")

    main(["--file", str(deck_path), "--mode", "sequential"])

    assert "Total Questions:" not in capsys.readouterr().out


def test_empty_deck_shows_zero_statistics_when_requested(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Handle an empty deck and optionally show zero statistics."""
    deck_path = tmp_path / "empty_deck.json"
    write_deck(deck_path, [])

    def unexpected_input(_prompt: str) -> str:
        pytest.fail("Input should not be requested for an empty deck.")

    monkeypatch.setattr("builtins.input", unexpected_input)

    result = main(["--file", str(deck_path), "--mode", "adaptive", "--stats"])

    output = capsys.readouterr().out
    assert result == 0
    assert "No flashcards available." in output
    assert "Total Questions: 0" in output
    assert "Accuracy: 0.0%" in output
    assert "Terms Missed: None" in output
