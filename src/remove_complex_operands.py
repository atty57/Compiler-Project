from collections.abc import Callable, Sequence
from functools import partial
import kernel
from kernel import Int, Add, Subtract, Multiply, Let, Var, Bool, If, LessThan, EqualTo, GreaterThanOrEqualTo
import monadic
from monadic import Atom


def remove_complex_operands(
    program: kernel.Program,
    fresh: Callable[[str], str],
) -> monadic.Program:
    return monadic.Program(
        program.parameters,
        rco_expr(program.body, fresh),
    )


type Binding = tuple[str, monadic.Expression]


def rco_expr(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
) -> monadic.Expression:
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

        case GreaterThanOrEqualTo(e1, e2):  # pragma: no branch
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap(b1, wrap(b2, GreaterThanOrEqualTo(a1, a2)))


def rco_atom(
    expr: kernel.Expression,
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


def wrap(
    bindings: Sequence[Binding],
    expr: monadic.Expression,
) -> monadic.Expression:
    for x, e in reversed(list(bindings)):
        expr = Let(x, e, expr)
    return expr
