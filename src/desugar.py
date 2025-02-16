from functools import partial
import sugar
from sugar import (
    Sum,
    Difference,
    Product,
    LetStar,
    Cond,
    Not,
    All,
    Any,
    NonAscending,
    Descending,
    Same,
    Ascending,
    NonDescending,
)
import kernel
from kernel import (
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
)


def desugar(
    program: sugar.Program,
) -> kernel.Program:
    return kernel.Program(
        parameters=program.parameters,
        body=desugar_expr(program.body),
    )


def desugar_expr(
    expr: sugar.Expression,
) -> kernel.Expression:
    recur = partial(desugar_expr)

    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            return Add(recur(e1), recur(e2))

        case Subtract(e1, e2):
            return Subtract(recur(e1), recur(e2))

        case Multiply(e1, e2):
            return Multiply(recur(e1), recur(e2))

        case Let(x, e1, e2):
            return Let(x, recur(e1), recur(e2))

        case Var():
            return expr

        case Bool():
            return expr

        case If(e1, e2, e3):
            return If(recur(e1), recur(e2), recur(e3))

        case LessThan(e1, e2):
            return LessThan(recur(e1), recur(e2))

        case EqualTo(e1, e2):
            return EqualTo(recur(e1), recur(e2))

        case GreaterThanOrEqualTo(e1, e2):
            return GreaterThanOrEqualTo(recur(e1), recur(e2))

        case _:
            raise NotImplementedError()
