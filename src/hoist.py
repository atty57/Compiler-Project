from collections.abc import Callable, Mapping
from functools import partial
import maltose
from maltose import (
    Lambda,
    Let,
    If,
    Apply,
    Halt,
)
import lactose
from lactose import Global


def hoist(
    program: maltose.Program,
    fresh: Callable[[str], str],
) -> lactose.Program:
    body, functions = hoist_statement(program.body, fresh)
    return lactose.Program(
        parameters=program.parameters,
        body=body,
        functions=functions,
    )


def hoist_statement(
    statement: maltose.Statement,
    fresh: Callable[[str], str],
) -> tuple[lactose.Statement, Mapping[str, Lambda[lactose.Statement]]]:
    recur = partial(hoist_statement, fresh=fresh)

    match statement:
        case Let(name, value, next):
            match value:
                case Lambda(parameters, body):
                    f = fresh("f")
                    body, fs1 = recur(body)
                    next, fs2 = recur(next)
                    return Let(name, Global(f), next), {**fs1, **fs2, f: Lambda(parameters, body)}

                case value:  # pragma: no branch
                    next, fs = recur(next)
                    return Let(name, value, next), fs

        case If(condition, then, otherwise):
            then, fs1 = recur(then)
            otherwise, fs2 = recur(otherwise)
            return If(condition, then, otherwise), {**fs1, **fs2}

        case Apply():
            return statement, {}

        case Halt():  # pragma: no branch
            return statement, {}
