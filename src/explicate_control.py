from collections.abc import Callable, Sequence
from functools import partial
import glucose
from glucose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Div,
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
from maltose import Copy, Halt


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
    expr = partial(explicate_control_expression, fresh=fresh)
    exprs = partial(explicate_control_expressions, fresh=fresh)

    match expression:
        case Int():
            return m(expression)

        case Add(x, y):
            t = fresh("t")
            return expr(
                x,
                lambda x: expr(
                    y,
                    lambda y: Let(t, Add(x, y), m(Var(t))),
                ),
            )

        case Subtract(x, y):
            t = fresh("t")
            return expr(
                x,
                lambda x: expr(
                    y,
                    lambda y: Let(t, Subtract(x, y), m(Var(t))),
                ),
            )

        case Multiply(x, y):
            t = fresh("t")
            return expr(
                x,
                lambda x: expr(
                    y,
                    lambda y: Let(t, Multiply(x, y), m(Var(t))),
                ),
            )

        case Div(x, y):
            t = fresh("t")
            return expr(
                x,
                lambda x_val: expr(  # Renamed to avoid clash if x, y are Vars
                    y,
                    # Corrected line:
                    lambda y_val: Let(t, Copy(Div(x_val, y_val)), m(Var(t))),
                ),
            )

        case Let(name, value, body):
            return expr(
                value,
                lambda value: Let(name, Copy(value), expr(body, m)),
            )

        case Var():
            return m(expression)

        case Bool():
            return m(expression)

        case If(condition, consequent, alternative):
            j = fresh("j")
            t = fresh("t")
            return Let(
                j,
                Lambda([t], m(Var(t))),
                expr(
                    condition,
                    lambda condition: If(
                        condition,
                        expr(consequent, lambda consequent: Apply(Var(j), [consequent])),
                        expr(alternative, lambda alternative: Apply(Var(j), [alternative])),
                    ),
                ),
            )

        case LessThan(x, y):
            t = fresh("t")
            return expr(
                x,
                lambda x: expr(
                    y,
                    lambda y: Let(t, LessThan(x, y), m(Var(t))),
                ),
            )

        case EqualTo(x, y):
            t = fresh("t")
            return expr(
                x,
                lambda x: expr(
                    y,
                    lambda y: Let(t, EqualTo(x, y), m(Var(t))),
                ),
            )

        case GreaterThanOrEqualTo(x, y):
            t = fresh("t")
            return expr(
                x,
                lambda x: expr(
                    y,
                    lambda y: Let(t, GreaterThanOrEqualTo(x, y), m(Var(t))),
                ),
            )

        case Unit():
            return m(expression)

        case Tuple(components):
            t = fresh("t")
            return exprs(
                components,
                lambda components: Let(t, Tuple(components), m(Var(t))),
            )

        case Get(base, index):
            t = fresh("t")
            return expr(
                base,
                lambda base: expr(
                    index,
                    lambda index: Let(t, Get(base, index), m(Var(t))),
                ),
            )

        case Set(base, index, value):
            t = fresh("t")
            return expr(
                base,
                lambda base: expr(
                    index,
                    lambda index: expr(
                        value,
                        lambda value: Let(t, Set(base, index, value), m(Var(t))),
                    ),
                ),
            )

        case Do(first, second):
            return expr(
                first,
                lambda _: expr(second, lambda second: m(second)),
            )

        case Lambda(parameters, body):
            t = fresh("t")
            k = fresh("k")
            return Let(
                t,
                Lambda([*parameters, k], expr(body, lambda body: Apply(Var(k), [body]))),
                m(Var(t)),
            )

        case Apply(callee, arguments):  # pragma: no branch
            t = fresh("t")
            k = fresh("k")
            return expr(
                callee,
                lambda callee: exprs(
                    arguments,
                    lambda arguments: Let(
                        k,
                        Lambda([t], m(Var(t))),
                        Apply(callee, [*arguments, Var(k)]),
                    ),
                ),
            )


def explicate_control_expressions(
    expressions: Sequence[glucose.Expression],
    k: Callable[[Sequence[maltose.Atom]], maltose.Statement],
    fresh: Callable[[str], str],
) -> maltose.Statement:
    expr = partial(explicate_control_expression, fresh=fresh)
    exprs = partial(explicate_control_expressions, fresh=fresh)
    match expressions:
        case []:
            return k([])
        case [x, *es]:
            return expr(x, lambda x: exprs(es, lambda vs: k([x, *vs])))
        case _:  # pragma: no cover
            raise NotImplementedError()
