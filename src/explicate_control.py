from collections.abc import Callable
from functools import partial
import maltose
from maltose import (
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
)
import lactose
from lactose import Block, Assign, Return, Jump


def explicate_control(
    program: maltose.Program,
    fresh: Callable[[str], str],
) -> lactose.Program:
    return lactose.Program(
        program.parameters,
        explicate_control_tail(program.body, fresh),
    )


def explicate_control_tail(
    expr: maltose.Expression,
    fresh: Callable[[str], str],
) -> lactose.Tail:
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

        case Tuple():
            return Return(expr)

        case Get():
            return Return(expr)

        case Set():
            return effect(expr, Return(Unit()))

        case Do(e1, e2):
            return effect(e1, tail(e2))

        case While():  # pragma: no branch
            return effect(expr, Return(Unit()))


def explicate_control_assign(
    dest: str,
    value: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
) -> lactose.Tail:
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)
    effect = partial(explicate_control_effect, fresh=fresh)

    match value:
        case Int():
            return Do(Assign(dest, value), next)

        case Add() | Subtract() | Multiply():
            return Do(Assign(dest, value), next)

        case Let(x, e1, e2):
            return assign(x, e1, assign(dest, e2, next))

        case Var():
            return Do(Assign(dest, value), next)

        case Bool():
            return Do(Assign(dest, value), next)

        case If(e1, e2, e3):
            return predicate(e1, assign(dest, e2, next), assign(dest, e3, next))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():
            return Do(Assign(dest, value), next)

        case Unit():
            return Do(Assign(dest, value), next)

        case Tuple():
            return Do(Assign(dest, value), next)

        case Get():
            return Do(Assign(dest, value), next)

        case Set():
            return effect(value, assign(dest, Unit(), next))

        case Do(e1, e2):
            return effect(e1, assign(dest, e2, next))

        case While():  # pragma: no branch
            return effect(value, assign(dest, Unit(), next))


def explicate_control_predicate(
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> lactose.Tail:
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)
    effect = partial(explicate_control_effect, fresh=fresh)

    match expr:
        case Int() | Add() | Subtract() | Multiply():
            raise ValueError(f"non-boolean predicate: {expr}")

        case Let(x, e1, e2):
            return assign(x, e1, predicate(e2, then, otherwise))

        case Var():
            ifTrue = fresh("then")
            ifFalse = fresh("else")
            return Do(
                Assign(ifTrue, Block(then)),
                Do(
                    Assign(ifFalse, Block(otherwise)),
                    If(expr, Jump(ifTrue), Jump(ifFalse)),
                ),
            )

        case Bool(b):
            match b:
                case True:
                    return then
                case False:  # pragma: no branch
                    return otherwise

        case If(e1, e2, e3):
            return predicate(e1, predicate(e2, then, otherwise), predicate(e3, then, otherwise))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():
            tmp = fresh("t")
            return assign(tmp, expr, predicate(Var(tmp), then, otherwise))

        case Unit():
            raise ValueError(f"non-boolean predicate: {expr}")

        case Tuple():
            raise ValueError(f"non-boolean predicate: {expr}")

        case Get():
            tmp = fresh("t")
            return assign(tmp, expr, predicate(Var(tmp), then, otherwise))

        case Set():
            raise ValueError(f"non-boolean predicate: {expr}")

        case Do(e1, e2):
            return effect(e1, predicate(e2, then, otherwise))

        case While():  # pragma: no branch
            raise ValueError(f"non-boolean predicate: {expr}")


def explicate_control_effect(
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
) -> lactose.Tail:
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)
    effect = partial(explicate_control_effect, fresh=fresh)

    match expr:
        case Int() | Add() | Subtract() | Multiply():
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

        case Tuple():
            return next

        case Get():
            return next

        case Set():
            return Do(expr, next)

        case Do(e1, e2):
            return effect(e1, effect(e2, next))

        case While(e1, e2):  # pragma: no branch
            loop = fresh("loop")
            return Do(
                Assign(loop, Block(predicate(e1, effect(e2, Jump(loop)), next))),
                Jump(loop),
            )
