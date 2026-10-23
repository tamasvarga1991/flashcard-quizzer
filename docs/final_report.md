# AI-Assisted Development Project Report

**Student Name:** Tamas Varga  
**Project Title:** Flashcard Quizzer  
**Date:** 2026-10-23

## Executive Summary

Flashcard Quizzer is a Python command-line application for studying JSON decks. It validates cards, quizzes users in sequential, random, or adaptive modes, and can report session statistics.

I used GitHub Copilot for planning, implementation, review, and refinement. Separating analysis-only prompts from modification requests kept scope decisions visible. Final verification passed 48 tests with 99.53% project-wide coverage; Black, mypy, flake8, and isort also passed.

## Project Overview

### Problem Statement

The project lets users study terms from JSON decks without editing application code for each deck.

### Solution Approach

Phase 1 added `utils/file_handler.py` to load both supported JSON formats, validate string-valued `front` and `back` fields, preserve additional fields, and report file or data errors through `FlashcardLoadError`. Phase 2 added the abstract `QuizMode` strategies, a delegating `QuizEngine`, and a factory for mode selection. `main.py` connects them with required file and mode arguments and optional `--stats`.

### Final Features

Sequential mode follows source order, Random mode shuffles a copy and serves every card once, and Adaptive mode requeues missed cards at the front until correct. The CLI compares trimmed answers case-insensitively, displays colored feedback, and supports `exit` and Ctrl+C. Optional statistics report answered attempts, accuracy, and unique missed front terms, including partial results after early termination.

## AI Collaboration Experience

### AI Tools Used and Workflow

GitHub Copilot was the AI assistant recorded in the project log. I used a sequence of planning, implementation, review, refinement, and verification rather than one large prompt. Planning and review requests explicitly prohibited file changes; implementation requests set scope and acceptance criteria. I checked suggestions against the requirements and made the final decisions about behavior.

### Most Valuable Interactions

During Phase 1 planning, Copilot identified unresolved validation choices before editing. I decided that `front` and `back` must be strings, while empty strings and empty decks remain valid and additional fields are preserved. In a later no-edit review, Copilot found that invalid UTF-8 could escape as `UnicodeDecodeError`; I accepted the focused error-handling change and regression test.

In Phase 2, Copilot initially proposed a one-retry limit for missed adaptive cards. I rejected that limit because the requirement called for incorrect cards to remain prioritized until answered correctly. The final strategy tracks original card indices, which also keeps identical-content cards distinct. During review, I accepted state-transition and immutability test improvements but declined case-insensitive factory names and an optional multi-missed-card scenario.

In Phase 3, Copilot implemented the CLI and integration tests around the existing loader, factory, and engine. Later, review led to stronger Ctrl+C assertions, partial-statistics tests, and an adaptive CLI test; no production changes were needed for that refinement.

In Phase 4, the AI's assessment found formatting and import-order issues despite 48 passing tests and 99.53% coverage. I chose not to add artificial tests for 100%. Black formatting and import sorting were applied without behavior changes, then `setup.cfg` aligned flake8 and isort with the project style. The Phase 5 audit confirmed the application and quality gates, identified the remaining README, report, and coverage-evidence work, and surfaced the report-template word-count conflict. I followed the authoritative 1,000-1,500-word requirement.

## Software Engineering Practices

### Design and Code Structure

The Strategy Pattern gives each mode a shared scheduling interface with a different algorithm; the Factory keeps mode-name selection out of the engine. `file_handler.py` owns loading and validation, `quiz_modes.py` owns strategies and engine behavior, and `main.py` owns arguments and terminal interaction. This separates concerns without a framework or runtime dependency.

The public functions and classes use type hints and docstrings. The CLI handles `FlashcardLoadError` at its boundary, and tests use temporary files, monkeypatched input, and captured output rather than requiring a real interactive session. Tests were written alongside the implementation, but the log does not establish a consistent test-first process, so I do not claim strict TDD.

### Testing Strategy

The pytest suite covers both loader formats, malformed and invalid data, mode scheduling, duplicate cards, adaptive retries, factory behavior, command-line validation, a complete three-question session, partial statistics, exit, Ctrl+C, and empty decks. `test_full_session`, `test_quiz_mode_factory`, and `test_adaptive_mode_behavior` cover the required integration and strategy behaviors. The final run passed all 48 tests.

## Technical Challenges and Solutions

The UTF-8 review found that invalid bytes were not translated into the loader's application-specific error; a focused regression test was added. The adaptive retry proposal was plausible in isolation but conflicted with the requirement, so I rejected its one-retry limit. Quality checks also exposed differing Black/flake8 line lengths and isort formatting. `setup.cfg` aligned the tools at 88 characters and the Black profile. An initial pytest command used an interpreter without pytest; switching to the existing `venv` resolved that issue.

## Code Quality Analysis

The final project-wide coverage result is **99.53%** (427 of 429 measured statements covered using `--cov=.`). The remaining statements are the script-entry guard and an intentional test failure sentinel, not untested quiz or loader behavior. I chose not to add artificial tests solely to move the result to 100%. The final checks passed: Black, mypy, bare flake8, and isort. The CLI help command and the sequential and adaptive sample-deck commands were also verified with controlled input.

For self-assessment, I consider the clearest evidence of maintainability the separation between loading, scheduling, mode construction, and CLI handling, together with tests for both success and failure cases. I have not assigned numerical ratings: those are personal judgments not established by repository metrics.

## Learning Outcomes

I learned that effective AI engineering is not about creating one huge perfect prompt. A controlled sequence of planning, implementation, review, refinement, and verification produced better results. Separating analysis prompts from modification prompts made scope and user decisions easier to preserve.

I want AI to do substantial implementation work, but architecture, requirements interpretation, scope, and final technical decisions still require human judgment. The one-retry proposal demonstrated this directly: the code idea was technically plausible, but it did not deliver the adaptive behavior the requirement described. The UTF-8 finding also showed that a passing suite cannot prove every edge case has been considered; independent review remains useful.

I also learned not to accept every recommendation automatically. I accepted tests that covered real contracts, but rejected unnecessary changes such as case-insensitive factory names, nonessential test expansion, and artificial coverage work. The most useful lesson for future projects is to give AI clear context, boundaries, acceptance criteria, and verification requirements while remaining responsible for deciding what is appropriate.

## Reflection

The most effective parts of the process were the no-edit planning and review steps, followed by small implementation requests and focused verification. Concrete examples made review productive: the UTF-8 issue became a regression test, the adaptive retry policy was checked against the requirement, and formatter disagreements led to shared configuration rather than hand-edited code to satisfy incompatible defaults.

The project also showed that software can be functionally complete while submission documentation remains unfinished. The README was updated during Phase 6, and this report records the final quality results. Coverage was measured and its percentage is included here; any separately required coverage artifact should be included with the submission materials.

### Future Enhancements

No specific future product features were selected in the documented phases. Any further work should be based on course requirements or user feedback rather than presented here as an existing commitment.

## Conclusion

Flashcard Quizzer now has a tested data layer, interchangeable quiz strategies, and a usable CLI. The project demonstrates that AI can accelerate implementation when prompts are specific, but careful human review is still necessary to interpret requirements, reject mismatched suggestions, and verify the finished work.

## Appendices

**Appendix A:** The phase-by-phase prompts, decisions, and outcomes are recorded in `docs/ai_edit_log.md`.  
**Appendix B:** Final verification: 48 tests passed; project-wide coverage was 99.53%; Black, mypy, flake8, and isort passed.  
**Appendix C:** Project-provided design-pattern and AI review guides informed implementation and review; no external resources are claimed here.