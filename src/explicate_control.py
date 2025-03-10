from collections.abc import Callable, Sequence
from functools import partial
import glucose
from glucose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Var,
    Let,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    Lambda,
    Apply,
)
import maltose
from maltose import (
    Copy,
    Halt,
)


def explicate_control(
    program: glucose.Program,
    fresh: Callable[[str], str],
) -> maltose.Program:
    return maltose.Program(
        parameters=program.parameters,
        body=explicate_control_expression(program.body, lambda v: Halt(v), fresh),
    )


def explicate_control_expression(
    expression: glucose.Expression,
    m: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
) -> maltose.Statement:
    recur = partial(explicate_control_expression, fresh=fresh)
    exprs = partial(explicate_control_expressions, fresh=fresh)

    match expression:
        case _:
            raise NotImplementedError()


def explicate_control_expressions(
    expressions: Sequence[glucose.Expression],
    k: Callable[[Sequence[maltose.Atom]], maltose.Statement],
    fresh: Callable[[str], str],
) -> maltose.Statement:
    expr = partial(explicate_control_expression, fresh=fresh)
    recur = partial(explicate_control_expressions, fresh=fresh)
    match expressions:
        case []:
            return k([])
        case [x, *es]:
            return expr(x, lambda x: recur(es, lambda vs: k([x, *vs])))
        case _:  # pragma: no cover
            raise NotImplementedError()
