from collections.abc import Callable
from functools import partial
import monadic
from monadic import (
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
    Cell,
    Get,
    Set,
    While,
)
import cps
from cps import Block, Assign, Seq, Return, Jump, Branch


def explicate_control(
    program: monadic.Program,
    fresh: Callable[[str], str],
) -> cps.Program:
    return cps.Program(
        program.parameters,
        explicate_control_tail(program.body, fresh),
    )


def explicate_control_tail(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
) -> cps.Tail:
    tail = partial(explicate_control_tail, fresh=fresh)
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)
    effect = partial(explicate_control_effect, fresh=fresh)

    match expr:
        case Int() | Add() | Subtract() | Multiply():
            return Return(expr)

        case Let(x, e1, e2):
            return assign(x, e1, tail(e2))

        case Var():
            return Return(expr)

        case Bool():
            return Return(expr)

        case If(e1, e2, e3):
            return predicate(e1, tail(e2), tail(e3))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():
            return Return(expr)

        case Unit():
            return Return(expr)

        case Cell():
            return Return(expr)

        case Get():
            return Return(expr)

        case Set():
            return effect(expr, Return(Unit()))

        case While():  # pragma: no branch
            return effect(expr, Return(Unit()))


def explicate_control_assign(
    dest: str,
    value: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)
    effect = partial(explicate_control_effect, fresh=fresh)

    match value:
        case Int():
            return Seq(Assign(dest, value), next)

        case Add() | Subtract() | Multiply():
            return Seq(Assign(dest, value), next)

        case Var():
            return Seq(Assign(dest, value), next)

        case Bool():
            return Seq(Assign(dest, value), next)

        case Let(x, e1, e2):
            return assign(x, e1, assign(dest, e2, next))

        case If(e1, e2, e3):
            return predicate(e1, assign(dest, e2, next), assign(dest, e3, next))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():
            return Seq(Assign(dest, value), next)

        case Unit():
            return Seq(Assign(dest, value), next)

        case Cell():
            return Seq(Assign(dest, value), next)

        case Get():
            return Seq(Assign(dest, value), next)

        case Set():
            return effect(value, assign(dest, Unit(), next))

        case While():  # pragma: no branch
            return effect(value, assign(dest, Unit(), next))


def explicate_control_predicate(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)

    match expr:
        case Int() | Add() | Subtract() | Multiply():  # pragma: no cover
            raise ValueError(f"non-boolean predicate: {expr}")

        case Let(x, e1, e2):
            return assign(x, e1, predicate(e2, then, otherwise))

        case Var():
            ifTrue = fresh("then")
            ifFalse = fresh("else")
            return Seq(
                Assign(ifTrue, Block(then)),
                Seq(
                    Assign(ifFalse, Block(otherwise)),
                    Branch(expr, Jump(ifTrue), Jump(ifFalse)),
                ),
            )

        case Bool(b):
            match b:
                case True:
                    return then
                case False:
                    return otherwise

        case If(e1, e2, e3):
            return predicate(e1, predicate(e2, then, otherwise), predicate(e3, then, otherwise))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():
            tmp = fresh("t")
            return assign(tmp, expr, predicate(Var(tmp), then, otherwise))

        case Unit():  # pragma: no cover
            raise ValueError(f"non-boolean predicate: {expr}")

        case Cell():  # pragma: no cover
            raise ValueError(f"non-boolean predicate: {expr}")

        case Get():
            tmp = fresh("t")
            return assign(tmp, expr, predicate(Var(tmp), then, otherwise))

        case Set():  # pragma: no cover
            raise ValueError(f"non-boolean predicate: {expr}")

        case While():  # pragma: no cover
            raise ValueError(f"non-boolean predicate: {expr}")


def explicate_control_effect(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)
    effect = partial(explicate_control_effect, fresh=fresh)

    match expr:
        case Int() | Add() | Subtract() | Multiply():  # pragma: no cover
            return next

        case Let(x, e1, e2):
            return assign(x, e1, effect(e2, next))

        case Var():
            return next

        case Bool():
            return next

        case If(e1, e2, e3):
            return predicate(e1, effect(e2, next), effect(e3, next))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():
            return next

        case Unit():
            return next

        case Cell():
            return next

        case Get():
            return next

        case Set():
            return Seq(expr, next)

        case While(e1, e2):  # pragma: no cover
            loop = fresh("loop")
            return Seq(
                Assign(loop, Block(predicate(e1, effect(e2, Jump(loop)), next))),
                Jump(loop),
            )
