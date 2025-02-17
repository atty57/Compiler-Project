from collections.abc import Callable
from functools import partial
import monadic
from monadic import Int, Add, Subtract, Multiply, Let, Var, Bool, If, LessThan, EqualTo, GreaterThanOrEqualTo
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

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():  # pragma: no branch
            return Return(expr)


def explicate_control_assign(
    dest: str,
    value: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(explicate_control_assign, fresh=fresh)
    predicate = partial(explicate_control_predicate, fresh=fresh)

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

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():  # pragma: no branch
            return Seq(Assign(dest, value), next)


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

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():  # pragma: no branch
            tmp = fresh("t")
            return assign(tmp, expr, predicate(Var(tmp), then, otherwise))
