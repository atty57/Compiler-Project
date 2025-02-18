from functools import partial
import sucrose
from sucrose import (
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
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    While,
    Assign,
)
import glucose


def convert_assign(
    program: sucrose.Program,
) -> glucose.Program:
    vars = mutable_variables(program.body)
    return glucose.Program(
        program.parameters,
        _wrap_vars(vars, convert_assign_expr(program.body, vars)),
    )


def convert_assign_expr(
    expr: sucrose.Expression,
    vars: set[str],
) -> glucose.Expression:
    recur = partial(convert_assign_expr, vars=vars)

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
            (vars_m, vars_u) = _partition({x}, e2)
            local_m = (vars | vars_m) - vars_u
            return Let(x, _maybe_cell(x, vars_m, recur(e1)), recur(e2, vars=local_m))

        case Var(x):
            return Get(expr, 0) if x in vars else expr

        case Bool():
            return expr

        case If(condition, consequent, alternative):
            return If(recur(condition), recur(consequent), recur(alternative))

        case LessThan(e1, e2):
            return LessThan(recur(e1), recur(e2))

        case EqualTo(e1, e2):
            return EqualTo(recur(e1), recur(e2))

        case GreaterThanOrEqualTo(e1, e2):
            return GreaterThanOrEqualTo(recur(e1), recur(e2))

        case Unit():
            return expr

        case Tuple(es):
            return Tuple([recur(e) for e in es])

        case Get(e1, i):
            return Get(recur(e1), i)

        case Set(e1, i, e2):
            return Set(recur(e1), i, recur(e2))

        case Do(e1, e2):
            return Do(recur(e1), recur(e2))

        case While(e1, e2):
            return While(recur(e1), recur(e2))

        case Assign(x, e1):  # pragma: no branch
            return Set(Var(x), 0, recur(e1))


def _wrap_vars(
    vars: set[str],
    expr: glucose.Expression,
) -> glucose.Expression:
    for v in vars:
        expr = Let(v, Tuple([Var(v)]), expr)
    return expr


def _partition(
    vars: set[str],
    *exprs: sucrose.Expression,
) -> tuple[set[str], set[str]]:
    mv = {mv for e in exprs for mv in mutable_variables(e)}
    return (vars & mv, vars - mv)


def _maybe_cell(
    name: str,
    vars: set[str],
    expr: glucose.Expression,
) -> glucose.Expression:
    return Tuple([expr]) if name in vars else expr


def mutable_variables(
    expr: sucrose.Expression,
) -> set[str]:
    recur = partial(mutable_variables)

    match expr:
        case Int():
            return set()

        case Add(e1, e2) | Subtract(e1, e2) | Multiply(e1, e2):
            return recur(e1) | recur(e2)

        case Let(x, e1, e2):
            return recur(e1) | (recur(e2) - {x})

        case Var():
            return set()

        case Bool():
            return set()

        case If(condition, consequent, alternative):
            return recur(condition) | recur(consequent) | recur(alternative)

        case LessThan(e1, e2) | EqualTo(e1, e2) | GreaterThanOrEqualTo(e1, e2):
            return recur(e1) | recur(e2)

        case Unit():
            return set()

        case Tuple(es):
            return {mv for e in es for mv in recur(e)}

        case Get(e1, _i):
            return recur(e1)

        case Set(e1, _i, e2):
            return recur(e1) | recur(e2)

        case Do(e1, e2):
            return recur(e1) | recur(e2)

        case While(e1, e2):
            return recur(e1) | recur(e2)

        case Assign(x, e1):  # pragma: no branch
            return {x} | recur(e1)
