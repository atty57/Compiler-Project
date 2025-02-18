from functools import partial
import sugar
from sugar import (
    Sum,
    Difference,
    Product,
    LetStar,
    Cond,
    Not,
    All,
    Any,
    NonAscending,
    Descending,
    Same,
    Ascending,
    NonDescending,
    Begin,
)
import kernel
from kernel import (
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
    Set,
    Get,
    While,
)


def desugar(
    program: sugar.Program,
) -> kernel.Program:
    return kernel.Program(
        parameters=program.parameters,
        body=desugar_expr(program.body),
    )


def desugar_expr(
    expr: sugar.Expression,
) -> kernel.Expression:
    recur = partial(desugar_expr)

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
            return Let(x, recur(e1), recur(e2))

        case Var():
            return expr

        case Bool():
            return expr

        case If(e1, e2, e3):
            return If(recur(e1), recur(e2), recur(e3))

        case LessThan(e1, e2):
            return LessThan(recur(e1), recur(e2))

        case EqualTo(e1, e2):
            return EqualTo(recur(e1), recur(e2))

        case GreaterThanOrEqualTo(e1, e2):
            return GreaterThanOrEqualTo(recur(e1), recur(e2))

        case Unit():
            return expr

        case Cell(e1):
            return Cell(recur(e1))

        case Get(e1):
            return Get(recur(e1))

        case Set(e1, e2):
            return Set(recur(e1), recur(e2))

        case While(e1, e2):
            return While(recur(e1), recur(e2))

        case Sum(es):
            match es:
                case []:
                    return Int(0)
                case [first, *rest]:
                    return Add(recur(first), recur(Sum(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Difference(es):
            match es:
                case [first]:
                    return Subtract(Int(0), recur(first))
                case [first, second]:
                    return Subtract(recur(first), recur(second))
                case [first, *rest]:
                    return Subtract(recur(first), recur(Difference(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Product(es):
            match es:
                case []:
                    return Int(1)
                case [first, *rest]:
                    return Multiply(recur(first), recur(Product(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case LetStar(bindings, body):
            match bindings:
                case []:
                    return recur(body)
                case [[x, e1], *rest]:
                    return Let(x, recur(e1), recur(LetStar(rest, body)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return If(recur(e1), recur(e2), recur(Cond(rest, default)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Not(e1):
            return If(EqualTo(recur(e1), Bool(True)), Bool(False), Bool(True))

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

        # >
        case Descending(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return LessThan(recur(second), recur(first))
                case [first, second, *rest]:
                    return recur(All([Descending([first, second]), Descending([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        # >=
        case NonAscending(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return GreaterThanOrEqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(All([NonAscending([first, second]), NonAscending([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        # =
        case Same(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return EqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(All([Same([first, second]), Same([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        # <=
        case NonDescending(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return GreaterThanOrEqualTo(recur(second), recur(first))
                case [first, second, *rest]:
                    return recur(All([NonDescending([first, second]), NonDescending([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        # <
        case Ascending(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return LessThan(recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(All([Ascending([first, second]), Ascending([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Begin(effects, value):  # pragma: no branch
            match effects:
                case []:
                    return recur(value)
                case [first, *rest]:
                    return Let("_", recur(first), recur(Begin(rest, value)))
                case _:  # pragma: no cover
                    raise NotImplementedError()
