# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

### Entry Template
```
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Example Entry

> This entry shows the expected level of detail. It does **not** count toward your five required entries. Delete it before you submit.

### 2024-01-15 - Flashcard Loader Validation

**Context:** I needed a module that loads flashcards from a JSON file and rejects bad data with a clear message instead of a traceback.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Create `data_loader.py` with a function that loads flashcards from a JSON file. Support both a plain list of `{"front", "back"}` objects and a `{"cards": [...]}` wrapper. Raise a custom exception with a helpful message if the file is missing, the JSON is malformed, or a card has no `back`. Use type hints."

**AI Response:** Claude generated a `load_flashcards()` function and a `FlashcardLoadError` exception. It handled both JSON formats and a missing file, but it caught every exception with a bare `except:` and only checked for `front`.

**Changes Made:** 
- Replaced the bare `except:` with specific `FileNotFoundError` and `json.JSONDecodeError` handlers
- Added validation that every card has non-empty `front` and `back` strings
- Added the card's position to the error message so the user can find the bad entry

**Reasoning:** 
- A bare `except:` hides real bugs, including `KeyboardInterrupt`
- A card without a `back` would break the quiz loop later, far from the cause
- A message that names the bad card is far easier to act on

**Outcome:** The loader now rejects bad decks with one readable line, and `test_load_missing_required_field` passes.

**Lessons Learned:** 
- AI covered the happy path well but under-specified the error handling
- Naming the exact failure cases in the prompt produced better code than asking for "error handling"
- Each requirement in the prompt should map to a test

---

## Your Log Entries

### 2026-10-23 - Phase 1 Planning and Requirements Analysis

**Context:** I was starting the Flashcard Quizzer's Data Layer & Validation phase and wanted a minimal implementation plan based on the starter project.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I explicitly asked the AI not to modify any files, to inspect the starter project and relevant files, and to propose a simple Phase 1 plan covering files, responsibilities, error cases, tests, and ambiguities. I also excluded quiz modes and the CLI quiz loop.

**AI Response:** The AI inspected the README, sample decks, guidance, and empty utility/test directories. It proposed a loader in `utils/file_handler.py` and focused pytest coverage, and identified ambiguities about field value types, empty strings, empty decks, extra fields, and whether `main.py` should be changed at this stage.

**Changes Made:** No files were changed during this planning interaction. Human decisions for implementation were to require string-valued `front` and `back`, allow empty strings and empty decks, preserve additional card fields, and defer `main.py` changes to the later CLI phase.

**Reasoning:** The requirements did not prohibit empty content or extra fields, while explicitly requiring the two card fields. Keeping CLI behavior for its later phase maintained the requested scope.

**Outcome:** Phase 1 scope and decisions were clarified before implementation, with no project files modified.

**Lessons Learned:** A no-edit planning step surfaced small but consequential validation choices before code was written.

---

### 2026-10-23 - Phase 1 Implementation and Verification

**Context:** With the data format and validation decisions established, I asked the AI to implement the Phase 1 loader and its tests without modifying `main.py` or adding later-phase functionality.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** Implement `utils/file_handler.py` to load both supported JSON formats and validate required string fields, plus comprehensive pytest coverage for valid and invalid inputs. Keep empty strings/decks valid, preserve extra fields, and do not modify unrelated files or later-phase features.

**AI Response:** The AI created `utils/file_handler.py` with a `FlashcardLoadError` and `load_flashcards()` function, and created `tests/test_file_handler.py` with tests for both formats and validation/error cases.

**Changes Made:** The first test command used the active Python interpreter, which did not have pytest installed. The AI then used the existing project `venv` interpreter, where the suite passed. Initial flake8 output identified line-length and end-of-file formatting issues; the AI corrected those and reran the tests and lint.

**Reasoning:** The project already had a `venv` with pytest, so using it avoided changing or creating an environment. Lint findings were limited to formatting and were corrected before considering the implementation verified.

**Outcome:** Before the later UTF-8 refinement, all 22 Phase 1 tests passed and flake8 passed for the two Phase 1 files. `main.py` and unrelated starter files were not modified.

**Lessons Learned:** Confirm which interpreter has the project tools installed, and treat lint output as a verification step rather than assuming passing tests are sufficient.

---

### 2026-10-23 - Phase 1 Code Review and UTF-8 Refinement

**Context:** I asked for a review of the Phase 1 implementation against the requirements and review checklist, with an explicit instruction not to modify files during the review.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** Review the current loader and tests for correctness, validation, errors, simplicity, type hints, docstrings, test coverage, and checklist alignment. Do not change any files.

**AI Response:** The AI found that invalid UTF-8 could raise an uncaught `UnicodeDecodeError`, and recommended converting it to `FlashcardLoadError` with a focused regression test. It also mentioned an optional stylistic simplification of a string literal.

**Changes Made:** Human decision: accept the functional UTF-8 error-handling improvement, reject the optional stylistic refactoring as unnecessary, and continue deferring `main.py`. The AI then added explicit UTF-8 error handling in `utils/file_handler.py` and an invalid-byte regression test in `tests/test_file_handler.py`.

**Reasoning:** Invalid file encoding is another malformed-input case and should use the loader's application-specific error type. The stylistic change did not improve behavior enough to justify expanding the edit, and CLI integration remains outside Phase 1.

**Outcome:** The final Phase 1 suite passed with 23 tests, and flake8 passed for both Phase 1 files with no errors. No other files were changed during the refinement.

**Lessons Learned:** A review can find gaps that successful tests miss; converting the finding into a focused regression test makes the behavior explicit and durable.

---

### 2026-10-23 - Phase 2 Planning and Architecture Review

**Context:** I was preparing the Flashcard Quizzer's Core Logic & Design Patterns phase and wanted an implementation plan grounded in the current project.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I explicitly instructed the AI not to modify any files. I asked it to inspect the current implementation, tests, design-pattern guidance, review checklist, and project documentation, then propose a minimal Phase 2 plan without implementing the quiz loop or CLI.

**AI Response:** The AI proposed the Strategy Pattern with an abstract `QuizMode`, `SequentialMode`, `RandomMode`, `AdaptiveMode`, and a minimal `QuizEngine`, plus a Factory for mode selection. It initially recommended limiting an incorrectly answered card to one retry.

**Changes Made:** No files were changed during planning. Human decision: accept the proposed architecture, but reject the one-retry limit because incorrect cards must actually be repeated and remain eligible for prioritized repetition until answered correctly.

**Reasoning:** A fixed retry limit would stop prioritizing a card after a repeated wrong answer, contrary to the reviewed requirement. The strategy classes, engine boundary, and factory otherwise fit the requested scope.

**Outcome:** Phase 2 architecture and adaptive retry behavior were agreed before implementation.

**Lessons Learned:** Reviewing behavior requirements against a proposed policy can reveal where a seemingly simple limit would contradict the feature's intended behavior.

---

### 2026-10-23 - Phase 2 Implementation and Verification

**Context:** After agreeing on the architecture and unbounded-until-correct adaptive repetition, I asked the AI to implement the Phase 2 quiz strategies and tests.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** Implement the quiz modes, factory, minimal engine, and focused pytest coverage. Preserve Phase 1, keep CLI and later features out of scope, and ensure adaptive misses are prioritized repeatedly without a retry cap.

**AI Response:** The AI created `utils/quiz_modes.py`, `utils/quiz_mode_factory.py`, and `tests/test_quiz_modes.py`. The modes share the `QuizMode` interface, the factory selects a strategy by supported mode name, and `QuizEngine` delegates selection and answer feedback. `AdaptiveMode` schedules cards by original index so identical card contents remain distinct.

**Changes Made:** The AI implemented the planned Strategy and Factory patterns and added tests for the modes, adaptive behavior, factory selection, and empty decks. No Phase 1 files or `main.py` were changed.

**Reasoning:** Separate strategies keep scheduling behavior modular, while original indices make answer feedback unambiguous for cards with identical contents.

**Outcome:** The complete test suite passed with 34 tests, and flake8 passed for the Phase 2 files.

**Lessons Learned:** Representing cards by position preserves identity without adding a separate card model, and testing a strategy through observable card order verifies its behavior.

---

### 2026-10-23 - Phase 2 Code Review and Test Refinement

**Context:** I requested a review of the Phase 2 implementation against the requirements, reviewed design decisions, checklist, and design-pattern guidance.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I explicitly asked the AI to review `utils/quiz_modes.py`, `utils/quiz_mode_factory.py`, and `tests/test_quiz_modes.py` without creating, modifying, or deleting files.

**AI Response:** The AI found no blocking correctness issues. It recommended tests for adaptive state transitions, a stronger RandomMode immutability check, case-insensitive factory handling, and a scenario with multiple different missed cards.

**Changes Made:** Human decisions: accept the adaptive state-transition tests and stronger immutability verification; reject case-insensitive factory names because the specification does not require them; defer the optional multiple-missed-cards scenario. The AI changed only `tests/test_quiz_modes.py`; no production-code changes were required.

**Reasoning:** The accepted tests cover existing contract guards and verify both list and card-content immutability. Lowercase-only mode names and deferring the additional scenario keep the agreed scope unchanged.

**Outcome:** The complete test suite passed with 37 tests, and flake8 passed for all Phase 2 files.

**Lessons Learned:** Review suggestions should be checked against the actual requirements: some improve coverage directly, while others would expand behavior beyond the specification.

---

### 2026-10-23 - Phase 3 Planning and CLI Design

**Context:** I was preparing to integrate the data loader and quiz engine into a playable command-line application.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I explicitly instructed the AI not to modify any files. I asked it to inspect the current Phase 1 and Phase 2 implementation, tests, README, requirements, review checklist, and starter documentation, then propose a minimal Phase 3 plan.

**AI Response:** The AI proposed using `main.py` as the CLI boundary and reusing the existing Phase 1 loader and Phase 2 factory and engine. It identified ambiguities around whether file and mode arguments should be required or have defaults, whether `--stats` should be opt-in, how partial statistics should behave after early termination, and how missed terms should be represented.

**Changes Made:** No files were changed during planning. Human decisions: require both file and mode arguments, keep `--stats` optional, show partial statistics after `exit` or Ctrl+C when requested, count adaptive retries as answered questions, and keep missed terms unique in first-missed order.

**Reasoning:** These decisions define predictable CLI behavior while reusing the existing loader and engine contracts without adding a separate session framework.

**Outcome:** The Phase 3 CLI boundary and statistics behavior were agreed before implementation.

**Lessons Learned:** Explicitly resolving CLI and statistics behavior before implementation helps keep the interface consistent with the existing components.

---

### 2026-10-23 - Phase 3 Implementation and Verification

**Context:** After agreeing on the CLI behavior, I asked the AI to connect the existing components into an interactive application and add integration coverage.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** Implement the CLI in `main.py` with argparse, existing loader/factory/engine integration, interactive answer handling, feedback colors, graceful stopping, optional statistics, and CLI tests. Do not modify Phase 1 or Phase 2 code, README, or this log.

**AI Response:** The AI implemented `main.py` and created `tests/test_main.py`. It reused `load_flashcards()`, `create_quiz_mode()`, and `QuizEngine`, rather than duplicating their behavior. The CLI included argparse, case-insensitive answer comparison, ANSI Correct/Incorrect feedback, graceful `exit` and Ctrl+C handling, loader-error reporting, statistics, and empty-deck handling.

**Changes Made:** The AI added the Phase 3 entry point and its integration tests without changing Phase 1 or Phase 2 production files.

**Reasoning:** Keeping CLI orchestration at the application boundary lets the existing loader and strategy engine retain their separate responsibilities.

**Outcome:** Initial verification passed with 47 tests; flake8 passed for the Phase 3 files, and `python main.py --help` displayed the expected options.

**Lessons Learned:** An integration test can exercise parsing, loading, strategy selection, user answers, feedback, and statistics together without requiring a real terminal.

---

### 2026-10-23 - Phase 3 Code Review and Test Refinement

**Context:** I requested a review of the CLI implementation and tests against the Phase 3 requirements and project review guidance.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I explicitly instructed the AI to review `main.py` and `tests/test_main.py` without creating, modifying, or deleting any files.

**AI Response:** The AI found no required production-code corrections. It proposed optional test improvements, including stronger Ctrl+C traceback verification, partial-statistics checks after early termination, and an AdaptiveMode CLI integration test.

**Changes Made:** Human decisions: accept the stronger Ctrl+C verification, partial-statistics tests, and AdaptiveMode integration test; reject additional isolated required-argument tests and a dedicated short-flag test; keep `exit` reserved even if it matches a theoretical answer. The AI changed only `tests/test_main.py`; no production code changes were required.

**Reasoning:** These accepted tests cover behavior not demonstrated by the initial full-session test, while the rejected items would add coverage or behavior beyond the decisions needed for this phase.

**Outcome:** Final verification passed with 48 tests, and flake8 passed for the Phase 3 files.

**Lessons Learned:** Reviewing integration coverage separately from production behavior helped strengthen confidence without expanding the implementation.

---

### 2026-10-23 - Phase 4 Quality Assessment

**Context:** I began the quality assurance phase by asking for a read-only assessment of the complete project and its required quality gates.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I explicitly instructed the AI not to modify any files. I asked it to inspect the project and run the full test suite, coverage, Black check, mypy, flake8, and required CLI checks.

**AI Response:** The AI reported 48 passing tests, 99.53% overall coverage, and a passing mypy check. Flake8 passed when run with the project's 88-character line length. Black check reported six files that would be reformatted, and isort identified import-order differences.

**Changes Made:** No files were changed during the assessment. Human decision: do not add artificial tests merely to raise coverage from 99.53% to 100%; fix Black formatting and legitimate import-order issues only.

**Reasoning:** Coverage was already above the project target, and the two uncovered statements were not reasons to add artificial tests. Formatting and import order were the remaining actionable quality issues.

**Outcome:** The assessment identified the exact files and tool mismatches to address without changing application behavior.

**Lessons Learned:** Quality metrics should direct meaningful validation and cleanup, not encourage tests that only exercise otherwise intentional guard paths.

---

### 2026-10-23 - Phase 4 Formatting and Quality Refinement

**Context:** After the assessment, I asked the AI to resolve the reported formatting and import-order issues without changing behavior or logic.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** Apply Black to the six files that failed check mode and apply isort only to the files with reported import-order differences. Do not add tests or change application logic.

**AI Response:** The AI applied Black formatting and import-order formatting. The test suite remained at 48 passing tests and coverage remained 99.53%; Black and mypy passed after formatting.

**Changes Made:** The AI changed formatting in the six Black-flagged files and import order in the two isort-flagged files. No behavior, application logic, or test logic was changed.

**Reasoning:** Verification exposed a configuration mismatch: Black and the project style used 88 characters, while bare flake8 defaulted to 79. Default isort formatting also conflicted with Black.

**Outcome:** The formatting findings were resolved, and the remaining discrepancy was identified as a tool-configuration issue rather than a reason to manually reformat code against the project standard.

**Lessons Learned:** Compatible formatter profiles and shared line-length configuration help prevent tools from prescribing conflicting source layouts.

---

### 2026-10-23 - Phase 4 Quality-Tool Configuration Alignment

**Context:** I asked the AI to resolve the remaining Black, flake8, and isort configuration mismatch with a minimal project-level change.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** Configure flake8 to follow the project's 88-character line length, configure isort consistently with Black, and rerun the normal quality gates. Do not change application behavior or update project documentation.

**AI Response:** The AI changed only `setup.cfg`: flake8 uses the 88-character limit and excludes the local `venv`, while isort uses the Black profile.

**Changes Made:** Human decision: align the tools through project-level configuration rather than manually formatting code to satisfy conflicting defaults. No application behavior or test logic was changed.

**Reasoning:** The existing `.editorconfig` already specified 88 characters, but flake8 did not consume that setting. A single `setup.cfg` provides the tool-specific settings in one place.

**Outcome:** Final verification passed: 48 tests, 99.53% coverage, Black, mypy, bare flake8, and isort check-only.

**Lessons Learned:** Centralized tool configuration makes routine quality checks consistent with the project’s formatting standard.

---

### 2026-10-23 - Phase 5 Final Rubric Review and Pre-Submission Audit

**Context:** I requested a final audit of the complete Flashcard Quizzer project before submission.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I explicitly instructed the AI to inspect and assess the repository against the functional requirements, architecture and design patterns, CLI, testing and quality gates, AI collaboration evidence, and submission deliverables without creating, modifying, formatting, or deleting files.

**AI Response:** The AI found the functional, architecture, CLI, testing, and quality requirements satisfied. Verification confirmed 48 passing tests, 99.53% coverage, and passing Black, mypy, flake8, and isort checks. The required sequential and adaptive CLI examples were verified with controlled input. The AI identified that the README still contained starter-state information, the final report was not yet completed, and coverage evidence still needed to be included appropriately for submission. It also noted that the report template says 2,000-3,000 words, while the project instructions and rubric reviewed by the human specify 1,000-1,500 words.

**Changes Made:** No files were changed during the audit. Human decisions: use the explicit 1,000-1,500-word project/rubric requirement for the final report, update the README in Phase 6, preserve appropriate coverage evidence, and not add optional Bandit/Safety scans because they are not required by the project rubric.

**Reasoning:** The final audit confirmed the application and quality gates while separating those results from the documentation deliverables that remain. The human-reviewed project requirement is authoritative for the final report length; optional scans should not be treated as submission blockers.

**Outcome:** The application passed the audited functional and quality checks. The README and final report remain Phase 6 submission work, and the coverage result needs to be preserved in the submitted evidence. No files were changed during the audit itself.

**Lessons Learned:** A pre-submission audit should distinguish working software and verified quality gates from documentation and evidence that still need to be prepared.

---

### 2026-10-23 - Phase 6 Final Documentation and Submission Artifacts

**Context:** I prepared the final project documentation after the Phase 5 audit identified that the README, report, and coverage evidence needed to be completed for submission.

**AI Tool Used:** GitHub Copilot

**Prompt/Request:** I asked the AI to update the README based only on the current implementation, tests, requirements, and configuration, then to analyze the report template and propose a plan without writing the report. I later asked it to create the final report using the template structure and repository evidence, with a strict 1,000-1,500-word target.

**AI Response:** The AI replaced the README's starter-state content with verified features, setup instructions, usage examples, tests, quality checks, and project structure. Before report writing, it identified that the template's 2,000-3,000-word guidance conflicted with the authoritative project/rubric requirement of 1,000-1,500 words.

**Changes Made:** Human decision: follow the 1,000-1,500-word requirement while retaining useful template structure. I supplied the personal learning and reflection perspective so the AI would not invent personal experiences. The AI created `docs/final_report.md` at approximately 1,322 words, grounded in the repository and AI log. It documented the UTF-8 review, rejection of the AdaptiveMode one-retry limit, selective acceptance and rejection of suggestions, quality-tool configuration alignment, and the decision not to add artificial tests to move coverage from 99.53% to 100%.

**Reasoning:** The authoritative report limit takes precedence over the conflicting template footer. Personal reflections are the student's account, while technical claims and collaboration events must be supported by the code, test results, and edit log.

**Outcome:** A persistent `docs/coverage_report.txt` was generated. It records 48 passing tests and 429 measured statements with two missed; its terminal summary displays 99% because it rounds to a whole number, while the precise coverage check recorded 99.53%. No application functionality was changed during Phase 6.

**Lessons Learned:** Final documentation should distinguish verified technical evidence from personal reflection, resolve conflicting instructions using the authoritative rubric, and preserve quality evidence without changing application behavior.

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?**
2. **Where did you need to make the most modifications to AI suggestions?**
3. **What patterns did you notice in AI strengths and weaknesses?**
4. **How did your prompting technique improve over time?**
5. **What would you do differently in future AI collaborations?**

## Summary Statistics

At the end of your project, fill out these statistics:

- **Total AI interactions:** ___
- **Lines of AI-generated code used:** ___
- **Lines of AI-generated code modified:** ___
- **Most helpful AI interaction:** ___
- **Most challenging AI interaction:** ___
- **Biggest lesson learned:** ___

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.