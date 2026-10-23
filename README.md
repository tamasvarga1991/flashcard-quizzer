# Flashcard Quizzer

Flashcard Quizzer is a command-line application for studying JSON flashcard decks. Choose a sequential, random, or adaptive quiz mode, answer prompts in the terminal, and optionally review session statistics.

## Features

- Loads decks from either a top-level JSON array or an object containing a `cards` array.
- Validates that every card has string-valued `front` and `back` fields. Additional card fields are preserved; empty strings and empty decks are allowed.
- Provides sequential, random, and adaptive quiz modes. Sequential mode follows the source order; Random mode shuffles a copy and serves every card once; Adaptive mode prioritizes missed cards and repeats them until answered correctly.
- Uses the Strategy Pattern for quiz modes and a Factory to select a mode.
- Compares answers to the back of each card after trimming surrounding whitespace and ignoring letter case.
- Displays immediate green `Correct!` or red `Incorrect` feedback in ANSI-compatible terminals.
- Accepts `exit` (case-insensitive, with surrounding whitespace ignored) to stop a session. Ctrl+C also stops gracefully.
- Offers optional session statistics with `--stats`: total answered attempts, accuracy percentage, and unique missed front terms in first-missed order. Adaptive retries count as attempts. Statistics include answers recorded before `exit` or Ctrl+C.
- Reports file loading and validation errors without exposing a Python traceback.

## Flashcard Format

The loader supports both of these JSON formats:

```json
[
  {"front": "API", "back": "Application Programming Interface"}
]
```

```json
{
  "cards": [
    {"front": "API", "back": "Application Programming Interface"}
  ]
}
```

Sample decks are in `data/`.

## Requirements and Setup

Python 3.10 or newer is required. The application uses the Python standard library at runtime. `requirements.txt` installs the project's testing, formatting, linting, type-checking, documentation, and security tools, along with optional packages for advanced development.

Create and activate a virtual environment from the project directory, then install the requirements:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the environment with:

```bash
source venv/bin/activate
```

## Usage

Both the file and mode arguments are required. Supported modes are `sequential`, `random`, and `adaptive`.

```bash
python main.py --help
python main.py --mode sequential --file data/glossary.json
python main.py -m adaptive -f data/python_basics.json
python main.py --mode sequential --file data/glossary.json --stats
```

The application displays each card's front and waits for an answer. In adaptive mode, an incorrect card is repeated ahead of the remaining cards until it is answered correctly. Type `exit` to end the session; use `--stats` to display the results accumulated so far.

## Tests and Quality Checks

Run the complete pytest suite and generate terminal and HTML coverage reports:

```bash
python -m pytest
python -m pytest --cov=. --cov-report=term-missing --cov-report=html
```

The HTML coverage report is written to `htmlcov/index.html`.

Run the project's formatting, type-checking, linting, and import-order checks:

```bash
python -m black --check .
python -m mypy .
python -m flake8 .
python -m isort --check-only main.py utils tests
```

`setup.cfg` configures flake8 to use the project's 88-character line length and configures isort to follow Black's profile.

## Project Structure

```text
main.py                     CLI entry point and interactive session
utils/file_handler.py       JSON loading and flashcard validation
utils/quiz_modes.py         QuizMode strategies and QuizEngine
utils/quiz_mode_factory.py  Quiz mode factory
tests/                      Loader, strategy, factory, and CLI tests
data/                       Sample JSON flashcard decks
docs/ai_edit_log.md          AI collaboration and review log
docs/design_patterns.md      Strategy and Factory pattern reference
docs/report_template.md      Final report template
ai_guidance/                 Prompting and code review guidance
requirements.txt              Development and quality-tool dependencies
setup.cfg                     flake8 and isort configuration
```

GitHub Copilot was used during development. Prompts, AI suggestions, human decisions, reviews, and verification outcomes are documented in `docs/ai_edit_log.md`.

## License

[License](../../LICENSE.txt)