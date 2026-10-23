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