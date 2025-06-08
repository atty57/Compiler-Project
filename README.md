# 471c Compiler Project
## Project Overview

This project is a compiler for a custom functional/imperative programming language ("Fructose"). It is designed as a modular, extensible pipeline that takes source code through parsing, type inference, optimization, and code generation to LLVM IR, which can then be executed natively. The project demonstrates advanced compiler construction techniques and language design.

---

## Major Extensions

### 1. Safe Division by Zero
- **What Changed:**
  - Introduced a new AST node, `Div`, with a built-in zero-check. Any `Div(e₁, e₂)` computes ⌊e₁ / e₂⌋ or raises a clear division-by-zero error at compile time if both operands are constants.
- **Design & Implementation:**
  - **Parser/AST:** Extended the grammar and AST to support division.
  - **Constant Folding:** Folds literal divisions and raises errors for constant division by zero.
  - **Explicate Control:** Ensures correct sequencing and purity.
  - **Value Numbering:** Identifies and shares repeated identical divisions.
  - **Lowering:** Emits LLVM signed division; runtime division by zero traps at the machine level.
- **Testing:**
  - Comprehensive test suite for parsing, constant folding, value numbering, and integration.
  - 100% coverage for new logic.
- **Known Problems:**
  - No runtime zero-check for non-constant divisors; 0/0 is undefined at runtime; rounding and overflow semantics may differ from Python.

### 2. Constant Folding
- **What Changed:**
  - Added a dedicated pass (`constant_folding.py`) to evaluate arithmetic at compile time, replacing expressions like `3+5` or `10/2` with their results.
- **Design & Implementation:**
  - Placed after parsing and before value numbering.
  - Handles Add, Subtract, Multiply, Div, and applies simplification rules (e.g., x+0→x).
- **Testing:**
  - Extensive tests for arithmetic, identity, zero handling, control flow, and error cases.
  - All tests pass; compile-time division by zero raises an error.
- **Known Problems:**
  - Only constant expressions are checked for division by zero; no advanced algebraic simplification.

### 3. Value Numbering
- **What Changed:**
  - Added `value_numbering.py` to assign unique value numbers to subexpressions, eliminating redundant computation.
- **Design & Implementation:**
  - Uses string-based hashing of AST shape.
  - Local and global passes ensure sharing across blocks.
- **Testing:**
  - Tests for basic value numbering, hashing, and rebuilding expressions.
  - Integration tests confirm correct interaction with constant folding.
- **Known Problems:**
  - String keys may miss some semantically equivalent expressions; assumes a functional front end.

### 4. Pattern Matching
- **What Changed:**
  - Added a `match` construct to branch on the shape of values (literals, wildcards, variables, tuples, nested patterns).
- **Design & Implementation:**
  - **Parser/AST:** Extended grammar and AST with `Match` and pattern classes.
  - **Simplify Pass:** Lowers patterns to chains of `If` and `Let` expressions.
- **Testing:**
  - Dedicated test suite for all pattern forms and edge cases.
  - Manual and automated tests confirm correct lowering.
- **Known Problems:**
  - Only tuple patterns are supported; no exhaustiveness checking; performance and scoping could be improved.

### 5. Monomorphic Type Inference
- **What Changed:**
  - Added a type inference pass to automatically deduce types for all expressions (Int, Bool, Unit, Tuples).
- **Design & Implementation:**
  - Runs after assignment conversion, before control-flow lowering.
  - Generates and solves type constraints, annotates AST nodes, and reports errors with clear messages.
- **Testing:**
  - Positive and negative tests for all AST forms and edge cases.
  - All positive tests pass; negative tests fail with clear errors.
- **Known Problems:**
  - No polymorphic let-generalization; limited to monomorphic types; error messages may not always point to the exact source location.

---

## Key Features & Extensions

- **Pattern Matching:**
  - Supports rich pattern matching on integers, booleans, units, variables, wildcards, and tuples.
  - Syntax similar to modern functional languages (e.g., `match` expressions).
- **Mutable State & Imperative Constructs:**
  - Includes `set!` for mutation, `while` loops, and `begin` blocks for sequencing.
- **First-Class Functions & Closures:**
  - Lambda expressions, higher-order functions, and closure conversion.
- **Type Inference:**
  - Hindley-Milner style type inference for statically checking programs.
- **Optimizations:**
  - Constant folding, value numbering, dead code elimination, and more.
- **LLVM IR Output & Execution:**
  - Outputs LLVM IR and can execute it directly using JIT compilation.
- **Extensible Pipeline:**
  - Each compiler phase is modular, making it easy to add new features or optimizations.

---

## Example: Factorial Program

Example source file: `examples/factorial.fru`

```lisp
(program (n)
  (let ((ans 1))
    (begin
      (while 
        (> n 0)
        (begin
          (set! ans (* n ans))
          (set! n (- n 1))))
      ans)))
```

---

## Getting Started

### Prerequisites

1. Install [git](https://git-scm.com/downloads)
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Install Python (recommended: 3.10+)

   ```console
   uv python install
   ```

### Installation

1. Clone the repository
2. Install pre-commit hooks:
   ```console
   uv run pre-commit install
   ```
3. Install dependencies:
   ```console
   uv sync
   ```

---

## Usage

### Compile a Program

```console
python src/main.py examples/factorial.fru -o factorial.ll
```

### Run a Program Directly

```console
python src/main.py examples/factorial.fru --run --args 5
```

- The output will be the result of the program (e.g., `120` for factorial of 5).
- The generated LLVM IR is printed to the output file or stdout.

### Run Tests

```console
uv run pytest
```
- Test report: `report.html`
- Coverage report: `htmlcov/index.html`

---

## Project Structure

- `src/` — Compiler source code (parsing, type inference, optimization, codegen, etc.)
- `examples/` — Example programs in the custom language
- `tests/` — Unit and integration tests for all compiler phases
- `reports/` — Test and coverage reports

---

## How to Extend

- Add new language features by editing the grammar (`src/fructose.lark`) and updating the parser/transformer (`src/parse.py`).
- Implement new optimizations as separate modules and add them to the pipeline in `src/main.py`.
- Add new tests in the `tests/` directory to ensure correctness.

---

## Acknowledgements

This project was developed as a college course project for CISC471/671: Compiler Construction. It demonstrates advanced concepts in language design, type systems, and code generation.

---

    Test report is in `report.html`.
    Coverage report is in `htmlcov/index.html`.

