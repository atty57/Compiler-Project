from functools import partial
import sucrose
from sucrose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Div,
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
    Lambda,
    Apply,
    Assign,
)
import glucose


def convert_assignments(
    program: sucrose.Program,
) -> glucose.Program:
    vars = mutable_free_variables(program.body)
    return glucose.Program(
        program.parameters,
        body=_wrap_vars(vars, convert_assignments_expression(program.body, vars)),
    )


def convert_assignments_expression(
    expression: sucrose.Expression,
    vars: set[str],
) -> glucose.Expression:
    recur = partial(convert_assignments_expression, vars=vars)

    match expression:
        case Int():
            return expression

        case Add(x, y):
            return Add(recur(x), recur(y))

        case Subtract(x, y):
            return Subtract(recur(x), recur(y))

        case Multiply(x, y):
            return Multiply(recur(x), recur(y))

        case Div(x, y):
            return Div(recur(x), recur(y))

        case Let(name, value, body):
            (vars_m, vars_u) = _partition({name}, body)
            local_m = (vars | vars_m) - vars_u
            return Let(name, _maybe_cell(name, vars_m, recur(value)), recur(body, vars=local_m))

        case Var(x):
            return Get(expression, Int(0)) if x in vars else expression

        case Bool():
            return expression

        case If(condition, consequent, alternative):
            return If(recur(condition), recur(consequent), recur(alternative))

        case LessThan(x, y):
            return LessThan(recur(x), recur(y))

        case EqualTo(x, y):
            return EqualTo(recur(x), recur(y))

        case GreaterThanOrEqualTo(x, y):
            return GreaterThanOrEqualTo(recur(x), recur(y))

        case Unit():
            return expression

        case Tuple(components):
            return Tuple([recur(e) for e in components])

        case Get(base, offset):
            return Get(recur(base), recur(offset))

        case Set(base, offset, value):
            return Set(recur(base), recur(offset), recur(value))

        case Do(effect, value):
            return Do(recur(effect), recur(value))

        case Lambda(parameters, body):
            (vars_m, vars_u) = _partition(set(parameters), body)
            local_m = (vars | vars_m) - vars_u
            return Lambda(parameters, _wrap_vars(vars_m, recur(body, vars=local_m)))

        case Apply(callee, arguments):
            return Apply(recur(callee), [recur(e) for e in arguments])

        case Assign(name, value):  # pragma: no branch
            return Set(Var(name), Int(0), recur(value))


def _partition(
    vars: set[str],
    *exprs: sucrose.Expression,
) -> tuple[set[str], set[str]]:
    mv = {mv for e in exprs for mv in mutable_free_variables(e)}
    return (vars & mv, vars - mv)


def _wrap_vars(
    vars: set[str],
    expr: glucose.Expression,
) -> glucose.Expression:
    for v in vars:
        return Let(v, Tuple([Var(v)]), expr)
    return expr


def _maybe_cell(
    name: str,
    vars: set[str],
    expr: glucose.Expression,
) -> glucose.Expression:
    return Tuple([expr]) if name in vars else expr


def mutable_free_variables(
    expression: sucrose.Expression,
) -> set[str]:
    recur = partial(mutable_free_variables)

    match expression:
        case Int():
            return set()

        case Add(x, y) | Subtract(x, y) | Multiply(x, y) | Div(x, y):
            return recur(x) | recur(y)

        case Let(name, value, body):
            return recur(value) | (recur(body) - {name})

        case Var():
            return set()

        case Bool():
            return set()

        case If(condition, consequent, alternative):
            return recur(condition) | recur(consequent) | recur(alternative)

        case LessThan(x, y) | EqualTo(x, y) | GreaterThanOrEqualTo(x, y):
            return recur(x) | recur(y)

        case Unit():
            return set()

        case Tuple(components):
            return {mv for e in components for mv in recur(e)}

        case Get(base, offset):
            return recur(base) | recur(offset)

        case Set(base, offset, value):
            return recur(base) | recur(offset) | recur(value)

        case Do(effect, value):
            return recur(effect) | recur(value)

        case Lambda(parameters, body):
            return recur(body) - set(parameters)

        case Apply(callee, arguments):
            return recur(callee) | {mv for e in arguments for mv in recur(e)}

        case Assign(name, value):  # pragma: no branch
            return recur(value) | {name}
