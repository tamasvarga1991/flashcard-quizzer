# AI-Assisted Development Project Report

**Student Name:** Tamas Varga  
**Project Title:** Flashcard Quizzer  
**Date:** 2026-10-23

## Executive Summary

Flashcard Quizzer is a Python command-line application for studying validated JSON flashcard decks in sequential, random, or adaptive modes, with optional session statistics.

GitHub Copilot supported planning, implementation, review, and refinement. Separating analysis-only prompts from modification requests kept scope decisions visible. Final verification passed 48 tests at 99.53% project-wide coverage; Black, mypy, flake8, and isort passed.

## Project Overview

### Problem Statement

Users can study terms from JSON decks without editing application code for each deck.

### Solution Approach

Phase 1 added `utils/file_handler.py` to load both JSON formats, validate string-valued `front` and `back`, preserve extra fields, and report errors through `FlashcardLoadError`. Phase 2 added abstract `QuizMode` strategies, a delegating `QuizEngine`, and a mode factory. `main.py` connects them with required file/mode arguments and optional `--stats`.

### Final Features

Sequential mode follows source order, Random mode shuffles a copy and serves every card once, and Adaptive mode requeues missed cards at the front until correct. The CLI compares trimmed answers case-insensitively, displays colored feedback, and supports `exit` and Ctrl+C. Optional statistics report answered attempts, accuracy, and unique missed front terms, including partial results after early termination.

## AI Collaboration Experience

### AI Tools Used and Workflow

GitHub Copilot is the AI assistant documented in the project log. I used staged planning, implementation, review, refinement, and verification rather than one large prompt. Planning/review requests prohibited file changes; implementation requests defined scope and acceptance criteria. I checked suggestions against requirements and made final behavior decisions.

### Most Valuable Interactions

During Phase 1 planning, Copilot identified unresolved validation choices before editing. I decided that `front` and `back` must be strings, while empty strings and empty decks remain valid and additional fields are preserved. In a later no-edit review, Copilot found that invalid UTF-8 could escape as `UnicodeDecodeError`; I accepted the focused error-handling change and regression test.

In Phase 2, Copilot initially proposed a one-retry limit for missed adaptive cards. I rejected that limit because the requirement called for incorrect cards to remain prioritized until answered correctly. The final strategy tracks original card indices, which also keeps identical-content cards distinct. During review, I accepted state-transition and immutability test improvements but declined case-insensitive factory names and an optional multi-missed-card scenario.

In Phase 3, Copilot implemented the CLI and integration tests around the existing loader, factory, and engine. Later, review led to stronger Ctrl+C assertions, partial-statistics tests, and an adaptive CLI test; no production changes were needed for that refinement.

In Phase 4, the AI's assessment found formatting and import-order issues despite 48 passing tests and 99.53% coverage. I chose not to add artificial tests for 100%. Black formatting and import sorting were applied without behavior changes, then `setup.cfg` aligned flake8 and isort with the project style. The Phase 5 audit confirmed the application and quality gates, identified the remaining README, report, and coverage-evidence work, and surfaced the report-template word-count conflict. I followed the authoritative 1,000-1,500-word requirement.

## Software Engineering Practices

### Design and Code Structure

The Strategy Pattern gives each mode a shared scheduling interface with a different algorithm; the Factory keeps mode selection out of the engine. `file_handler.py` owns loading, `quiz_modes.py` owns scheduling, and `main.py` owns arguments and terminal interaction. This separates concerns without a runtime framework.

The public functions and classes use type hints and docstrings. The CLI handles `FlashcardLoadError` at its boundary, and tests use temporary files, monkeypatched input, and captured output rather than requiring a real interactive session. Tests were written alongside the implementation, but the log does not establish a consistent test-first process, so I do not claim strict TDD.

### Testing Strategy

Tests cover both loader formats, invalid data, mode scheduling, duplicate cards, adaptive retries, factory behavior, CLI validation, a three-question session, partial statistics, exit, Ctrl+C, and empty decks. The required `test_full_session`, `test_quiz_mode_factory`, and `test_adaptive_mode_behavior` are present. All 48 tests passed.

## Technical Challenges and Solutions

Review found invalid UTF-8 was not translated into the loader's application-specific error; a focused regression test was added. I rejected the proposed one-retry limit because it conflicted with the adaptive requirement. Quality checks exposed Black/flake8 line-length and isort formatting conflicts; `setup.cfg` aligned them at 88 characters and the Black profile. An initial interpreter lacked pytest, so the existing `venv` was used.

## Code Quality Analysis

The final project-wide coverage result is **99.53%** (427 of 429 measured statements covered using `--cov=.`). The remaining statements are the script-entry guard and an intentional test failure sentinel, not untested quiz or loader behavior. I chose not to add artificial tests solely to move the result to 100%. The final checks passed: Black, mypy, bare flake8, and isort. The CLI help command and the sequential and adaptive sample-deck commands were also verified with controlled input.

Production-code metrics use only `main.py`, `utils/file_handler.py`, `utils/quiz_modes.py`, and `utils/quiz_mode_factory.py`; tests, `__init__.py`, documentation, generated files, and virtual-environment files are excluded. These files contain **325 physical lines**, **19 function/method definitions**, and **6 class definitions**. Physical lines include blanks and comments; definitions were counted by parsing each file with Python AST.

**Linting score:** Not applicable—flake8 reports violations rather than a numeric linting score. The final bare flake8 check completed without errors.

These reflective self-assessment ratings are supported by the project evidence, not automated scores:

- **Code Readability: 5/5** — Responsibilities are separated across focused modules, with type hints and docstrings supporting comprehension.
- **Code Maintainability: 5/5** — Strategy and Factory patterns isolate quiz-mode behavior and allow another mode without redesigning the loader or CLI.
- **Test Quality: 5/5** — 48 tests pass, coverage is 99.53%, and tests meaningfully cover edge cases, errors, adaptive behavior, and CLI integration.
- **Documentation: 4/5** — README, AI log, coverage evidence, and report provide substantial documentation, but the first report omitted required template metrics and ratings identified by reviewer feedback.

## Learning Outcomes

I learned that effective AI engineering is not about creating one huge perfect prompt. A controlled sequence of planning, implementation, review, refinement, and verification produced better results. Separating analysis prompts from modification prompts made scope and user decisions easier to preserve.

I want AI to do substantial implementation work, but architecture, requirements interpretation, scope, and final technical decisions still require human judgment. The one-retry proposal demonstrated this directly: the code idea was technically plausible, but it did not deliver the adaptive behavior the requirement described. The UTF-8 finding also showed that a passing suite cannot prove every edge case has been considered; independent review remains useful.

I also learned not to accept every recommendation automatically. I accepted tests that covered real contracts, but rejected unnecessary changes such as case-insensitive factory names, nonessential test expansion, and artificial coverage work. The most useful lesson for future projects is to give AI clear context, boundaries, acceptance criteria, and verification requirements while remaining responsible for deciding what is appropriate.

## Reflection

No-edit planning/review followed by scoped implementation and verification worked well. Concrete review produced the UTF-8 regression test, clarified adaptive retries against requirements, and led to shared formatter configuration instead of conflicting manual formatting.

Next time, I would use the application as an end user earlier instead of relying primarily on tests, coverage, and code checks. Extensive automated verification passed before I personally exercised the full quiz experience. Automated checks are essential, but do not replace hands-on product validation. I would use: `Plan -> Generate -> Review -> Refine -> Verify -> Use it yourself -> Ship`.

### Future Enhancements

A possible future Spaced Repetition mode could extend the Strategy Pattern by scheduling cards using learning history across multiple sessions rather than only current-session mistakes. This is a proposal, not implemented functionality or a commitment.

## Conclusion

Flashcard Quizzer now has a tested data layer, interchangeable quiz strategies, and a usable CLI. The project demonstrates that AI can accelerate implementation when prompts are specific, but careful human review is still necessary to interpret requirements, reject mismatched suggestions, and verify the finished work.

## Appendices

**Appendix A:** The phase-by-phase prompts, decisions, and outcomes are recorded in `docs/ai_edit_log.md`.  
**Appendix B:** Final verification: 48 tests passed; project-wide coverage was 99.53%; Black, mypy, flake8, and isort passed.  
**Appendix C:** Project-provided design-pattern and AI review guides informed implementation and review; no external resources are claimed here.