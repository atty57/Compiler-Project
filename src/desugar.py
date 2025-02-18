from functools import partial
import fructose
from fructose import (
    Int,
    Let,
    Var,
    LetStar,
    Bool,
    Not,
    All,
    Any,
    If,
    Cond,
    Unit,
    Tuple,
    Get,
    Set,
    While,
    Assign,
    Cell,
    CellGet,
    CellSet,
    Vector,
    VectorLength,
    VectorGet,
    VectorSet,
)
import sucrose


def desugar(
    program: fructose.Program,
) -> sucrose.Program:
    return sucrose.Program(
        parameters=program.parameters,
        body=desugar_expr(program.body),
    )


def desugar_expr(
    expr: fructose.Expression,
) -> sucrose.Expression:
    recur = partial(desugar_expr)

    match expr:
        case Int():
            return expr

        case fructose.Add(es):
            match es:
                case []:
                    return Int(0)
                case [first, *rest]:
                    return sucrose.Add(recur(first), recur(fructose.Add(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.Subtract(es):
            match es:
                case [first]:
                    return sucrose.Subtract(Int(0), recur(first))
                case [first, second]:
                    return sucrose.Subtract(recur(first), recur(second))
                case [first, *rest]:
                    return sucrose.Subtract(recur(first), recur(fructose.Subtract(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.Multiply(es):
            match es:
                case []:
                    return Int(1)
                case [first, *rest]:
                    return sucrose.Multiply(recur(first), recur(fructose.Multiply(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Let(x, e1, e2):
            return Let(x, recur(e1), recur(e2))

        case Var():
            return expr

        case LetStar(bindings, body):
            match bindings:
                case []:
                    return recur(body)
                case [[x, e1], *rest]:
                    return Let(x, recur(e1), recur(LetStar(rest, body)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Bool():
            return expr

        case Not(e1):
            return If(sucrose.EqualTo(recur(e1), Bool(True)), Bool(False), Bool(True))

        case All(es):
            match es:
                case []:
                    return Bool(True)
                case [first, *rest]:
                    return If(recur(first), recur(All(rest)), Bool(False))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Any(es):
            match es:
                case []:
                    return Bool(False)
                case [first, *rest]:
                    return If(recur(first), Bool(True), recur(Any(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case If(e1, e2, e3):
            return If(recur(e1), recur(e2), recur(e3))

        case Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return If(recur(e1), recur(e2), recur(Cond(rest, default)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.LessThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return sucrose.GreaterThanOrEqualTo(recur(second), recur(first))
                case [first, second, *rest]:
                    return If(
                        sucrose.GreaterThanOrEqualTo(recur(second), recur(first)),
                        recur(fructose.LessThanOrEqualTo([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.LessThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return sucrose.LessThan(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        sucrose.LessThan(recur(first), recur(second)),
                        recur(fructose.LessThan([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.EqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return sucrose.EqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        sucrose.EqualTo(recur(first), recur(second)),
                        recur(fructose.EqualTo([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.GreaterThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return sucrose.LessThan(recur(second), recur(first))
                case [first, second, *rest]:
                    return If(
                        sucrose.LessThan(recur(second), recur(first)),
                        recur(fructose.GreaterThan([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.GreaterThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return sucrose.GreaterThanOrEqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        sucrose.GreaterThanOrEqualTo(recur(first), recur(second)),
                        recur(fructose.GreaterThanOrEqualTo([second, *rest])),
                        Bool(False),
                    )

                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Unit():
            return expr

        case Tuple(es):
            return Tuple([recur(e) for e in es])

        case Get(e1, i):
            return Get(recur(e1), i)

        case Set(e1, i, e2):
            return Set(recur(e1), i, recur(e2))

        case fructose.Do(es):
            match es:
                case []:
                    return Unit()
                case [first]:
                    return recur(first)
                case [first, *rest]:
                    return sucrose.Do(recur(first), recur(fructose.Do(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case While(e1, e2):
            return While(recur(e1), recur(e2))

        case Assign(x, e1):
            return Assign(x, recur(e1))

        case Cell(e1):
            return Tuple([recur(e1)])

        case CellGet(e1):
            return Get(recur(e1), 0)

        case CellSet(e1, e2):
            return Set(recur(e1), 0, recur(e2))

        case Vector(es):
            return Tuple([Int(len(es)), *[recur(e) for e in es]])

        case VectorLength(e1):
            return Get(recur(e1), 0)

        case VectorGet(e1, i):
            return Get(recur(e1), i + 1)

        case VectorSet(e1, i, e2):  # pragma: no branch
            return Set(recur(e1), i + 1, recur(e2))
