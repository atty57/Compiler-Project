from collections.abc import Callable, MutableMapping
from functools import partial
from glucose import (
    Program,
    Expression,
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
    Lambda,
    Apply,
)


def uniqify(
    program: Program,
    fresh: Callable[[str], str],
) -> Program:
    replacements = {parameter: fresh(parameter) for parameter in program.parameters}
    return Program(
        parameters=list(replacements.values()),
        body=uniqify_expression(program.body, replacements, fresh),
    )


def uniqify_expression(
    expression: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
) -> Expression:
    recur = partial(uniqify_expression, replacements=replacements, fresh=fresh)

    match expression:
        case Int():
            return expression

        case Add(x, y):
            return Add(recur(x), recur(y))

        case Subtract(x, y):
            return Subtract(recur(x), recur(y))

        case Multiply(x, y):
            return Multiply(recur(x), recur(y))

        case Let(name, value, body):
            replacement = fresh(name)
            return Let(replacement, recur(value), recur(body, replacements={**replacements, name: replacement}))

        case Var(x):
            return Var(replacements[x])

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

        case Get(tuple, index):
            return Get(recur(tuple), recur(index))

        case Set(tuple, index, value):
            return Set(recur(tuple), recur(index), recur(value))

        case Do(effect, value):
            return Do(recur(effect), recur(value))

        case Lambda(parameters, body):
            local = {parameter: fresh(parameter) for parameter in parameters}
            return Lambda(list(local.values()), recur(body, replacements={**replacements, **local}))

        case Apply(callee, arguments):  # pragma: no branch
            return Apply(recur(callee), [recur(e) for e in arguments])
