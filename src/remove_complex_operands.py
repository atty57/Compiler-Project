from collections.abc import Callable, Sequence
from functools import partial
from itertools import chain
import glucose
from glucose import (
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
    Lambda,
    Apply,
)
import maltose
from maltose import Atom


def remove_complex_operands(
    program: glucose.Program,
    fresh: Callable[[str], str],
) -> maltose.Program:
    return maltose.Program(
        program.parameters,
        rco_expr(program.body, fresh),
    )


type Binding = tuple[str, maltose.Expression]


def rco_expr(
    expr: glucose.Expression,
    fresh: Callable[[str], str],
) -> maltose.Expression:
    to_expr = partial(rco_expr, fresh=fresh)
    to_atom = partial(rco_atom, fresh=fresh)

    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b2, Add(a1, a2)))

        case Subtract(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b2, Subtract(a1, a2)))

        case Multiply(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b2, Multiply(a1, a2)))

        case Let(x, e1, e2):
            return Let(x, to_expr(e1), to_expr(e2))

        case Var():
            return expr

        case Bool():
            return expr

        case If(e1, e2, e3):
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            e3 = to_expr(e3)
            return If(e1, e2, e3)

        case LessThan(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b2, LessThan(a1, a2)))

        case EqualTo(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b2, EqualTo(a1, a2)))

        case GreaterThanOrEqualTo(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b2, GreaterThanOrEqualTo(a1, a2)))

        case Unit():
            return expr

        case Tuple(es):
            results = [to_atom(e) for e in es]
            as_ = [a for a, _ in results]
            bs = list(chain.from_iterable(bs for _, bs in results))
            return wrap(bs, Tuple(as_))

        case Get(e1, i):
            a1, b1 = to_atom(e1)
            return wrap(b1, Get(a1, i))

        case Set(e1, i, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b1, Set(a1, i, a2)))

        case Do(e1, e2):
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            return Do(e1, e2)

        case While(e1, e2):
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            return While(e1, e2)

        case Lambda(xs, e1):
            e1 = to_expr(e1)
            return Lambda(xs, e1)

        case Apply(e1, es):  # pragma: no branch
            results = [to_atom(e) for e in [e1, *es]]
            a1, *as_ = [a for a, _ in results]
            bs = list(chain.from_iterable(bs for _, bs in results))
            return wrap(bs, Apply(a1, as_))


def rco_atom(
    expr: glucose.Expression,
    fresh: Callable[[str], str],
) -> tuple[Atom, Sequence[Binding]]:
    to_expr = partial(rco_expr, fresh=fresh)
    to_atom = partial(rco_atom, fresh=fresh)

    match expr:
        case Int():
            return expr, []

        case Add(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return Var(tmp), [*b1, *b2, (tmp, Add(a1, a2))]

        case Subtract(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return Var(tmp), [*b1, *b2, (tmp, Subtract(a1, a2))]

        case Multiply(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return Var(tmp), [*b1, *b2, (tmp, Multiply(a1, a2))]

        case Let(x, e1, e2):
            a2, b2 = to_atom(e2)
            return a2, [(x, to_expr(e1)), *b2]

        case Var():
            return expr, []

        case Bool():
            return expr, []

        case If(e1, e2, e3):
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            e3 = to_expr(e3)
            tmp = fresh("t")
            return Var(tmp), [(tmp, If(e1, e2, e3))]

        case LessThan(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return Var(tmp), [*b1, *b2, (tmp, LessThan(a1, a2))]

        case EqualTo(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return Var(tmp), [*b1, *b2, (tmp, EqualTo(a1, a2))]

        case GreaterThanOrEqualTo(e1, e2):  # pragma: no branch
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return Var(tmp), [*b1, *b2, (tmp, GreaterThanOrEqualTo(a1, a2))]

        case Unit():
            return expr, []

        case Tuple(es):
            results = [to_atom(e) for e in es]
            as_ = [a for a, _ in results]
            bs = list(chain.from_iterable(bs for _, bs in results))
            tmp = fresh("t")
            return Var(tmp), [*bs, (tmp, Tuple(as_))]

        case Get(e1, i):
            a1, b1 = to_atom(e1)
            tmp = fresh("t")
            return Var(tmp), [*b1, (tmp, Get(a1, i))]

        case Set(e1, i, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return Var(tmp), [*b1, *b2, (tmp, Set(a1, i, a2))]

        case Do(e1, e2):
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            tmp = fresh("t")
            return Var(tmp), [(tmp, Do(e1, e2))]

        case While(e1, e2):  # pragma: no branch
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            tmp = fresh("t")
            return Var(tmp), [(tmp, While(e1, e2))]

        case Lambda(xs, e1):
            e1 = to_expr(e1)
            tmp = fresh("t")
            return Var(tmp), [(tmp, Lambda(xs, e1))]

        case Apply(e1, es):
            results = [to_atom(e) for e in [e1, *es]]
            a1, *as_ = [a for a, _ in results]
            bs = list(chain.from_iterable(bs for _, bs in results))
            tmp = fresh("t")
            return Var(tmp), [*bs, (tmp, Apply(a1, as_))]


def wrap(
    bindings: Sequence[Binding],
    expr: maltose.Expression,
) -> maltose.Expression:
    for x, e in reversed(list(bindings)):
        expr = Let(x, e, expr)
    return expr
