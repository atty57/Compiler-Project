from collections.abc import Callable
from functools import partial
from maltose import (
    Program,
    Atom,
    Int,
    Var,
    Bool,
    Unit,
    Expression,
    Add,
    Subtract,
    Multiply,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Lambda,
    Copy,
    Statement,
    Let,
    If,
    Apply,
    Halt,
)


def close(
    program: Program,
    fresh: Callable[[str], str],
) -> Program:
    return Program(
        program.parameters,
        close_statement(program.body, fresh),
    )


def close_statement(
    statement: Statement,
    fresh: Callable[[str], str],
) -> Statement:
    recur = partial(close_statement, fresh=fresh)
    match statement:
        case _:
            raise NotImplementedError()


def free_variables_statement(
    statement: Statement,
) -> set[str]:
    atom = partial(free_variables_atom)
    recur = partial(free_variables_statement)
    expr = partial(free_variables_expression)

    match statement:
        case _:
            raise NotImplementedError()


def free_variables_expression(
    expression: Expression,
) -> set[str]:
    atom = partial(free_variables_atom)
    stmt = partial(free_variables_statement)

    match expression:
        case _:
            raise NotImplementedError()


def free_variables_atom(
    atom: Atom,
) -> set[str]:
    match atom:
        case _:
            raise NotImplementedError()
