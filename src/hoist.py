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
        case _:
            raise NotImplementedError()
