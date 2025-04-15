# hoist.py
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Dict, Tuple

import maltose
from maltose import (
    Lambda,
    Let,
    If,
    Apply,
    Halt,
)
from lactose import (
    Program,
    Global,
)

# Type aliases to keep the signatures readable
Statement = maltose.Statement
FunctionMap = Dict[str, Lambda[Statement]]


def hoist_statement(
    statement: Statement,
    fresh: Callable[[str], str],
) -> Tuple[Statement, FunctionMap]:
    """
    Hoist every λ‑expression that appears directly in a `Let` binding.

    Returns a pair `(new_stmt, functions)` where

    * `new_stmt`  – the transformed statement with lambdas replaced by `Global`s
    * `functions` – a mapping from fresh global names to the lifted lambdas
    """
    match statement:
        # ──────────────────────────────────────────────────────────── LET ──
        case Let(var, value, body):
            if isinstance(value, Lambda):
                # Give the lambda a fresh top‑level name such as "_f0"
                fn_name = fresh("f")

                # First hoist inside the lambda's *body*
                lifted_body, inner_funcs = hoist_statement(value.body, fresh)
                lifted_abs: Lambda[Statement] = Lambda(value.parameters, lifted_body)

                # Then hoist inside the *rest* of the program
                new_body, rest_funcs = hoist_statement(body, fresh)

                return (
                    Let(var, Global(fn_name), new_body),
                    {fn_name: lifted_abs, **inner_funcs, **rest_funcs},
                )

            # Non‑lambda value: just recurse into the body
            new_body, funcs = hoist_statement(body, fresh)
            return (Let(var, value, new_body), funcs)

        # ───────────────────────────────────────────────────────────── IF ──
        case If(cond, then_stmt, else_stmt):
            then_h, funcs_then = hoist_statement(then_stmt, fresh)
            else_h, funcs_else = hoist_statement(else_stmt, fresh)
            return (If(cond, then_h, else_h), {**funcs_then, **funcs_else})

        # ─────────────────────────────────────────────────────────── APPLY ──
        case Apply(callee, args):
            return (Apply(callee, args), {})

        # ─────────────────────────────────────────────────────────── HALT ──
        case Halt(val):
            return (Halt(val), {})

        # ─────────────────────────────────────────────────────────── OTHER ──
        case _:
            raise NotImplementedError(
                f"hoist_statement: unhandled statement kind {type(statement)}"
            )


# ──────────────────────────────────────────────────────────────────────────
# Public entry‑point used by the compiler pipeline
# ──────────────────────────────────────────────────────────────────────────
def hoist(
    program: maltose.Program,
    fresh: Callable[[str], str],
) -> Program:
    """
    Lift all lambdas in a Maltose program to top‑level functions,
    producing a Lactose `Program` that carries a `functions` dictionary.
    """
    body, functions = hoist_statement(program.body, fresh)
    return Program(
        parameters=program.parameters,
        body=body,
        functions=functions,
    )
