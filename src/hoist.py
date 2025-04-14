from collections.abc import Callable
from typing import Dict, cast

from lactose import (
    Program,
    Lambda,
    Statement,
    Let,
    If,
    Apply,
    Halt,
    Global,
)


def hoist(program: Program, fresh: Callable[[str], str]) -> Program:
    """
    Hoist all lambda expressions to the top level, replacing them with references
    to global functions.
    """
    functions: Dict[str, Lambda[Statement]] = {}

    def hoist_statement(statement: Statement) -> Statement:
        """Recursively hoist lambdas in statements."""
        recur = hoist_statement

        match statement:
            case Let(name, value, body):
                if isinstance(value, Lambda):
                    # Hoist the lambda to top level
                    func_name = fresh("lambda")
                    functions[func_name] = Lambda[Statement](
                        value.parameters, hoist_statement(cast(Statement, value.body))
                    )
                    # Replace with global reference
                    return Let(name, Global(func_name), hoist_statement(body))
                else:
                    # Process other expressions normally
                    return Let(name, value, hoist_statement(body))

            case If(condition, then_branch, else_branch):
                return If(condition, recur(then_branch), recur(else_branch))

            case Apply(callee, arguments):
                return Apply(callee, arguments)

            case Halt(value):
                return Halt(value)

            case _:
                raise ValueError(f"Unhandled statement type: {type(statement)}")

    hoisted_body = hoist_statement(program.body)
    return Program(program.parameters, hoisted_body, functions)
