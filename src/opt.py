from functools import partial
from kernel import (
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
    Cell,
    Get,
    Set,
    Do,
    While,
)


def opt(
    program: Program,
) -> Program:
    return Program(
        parameters=program.parameters,
        body=opt_expr(program.body),
    )


def opt_expr(
    expr: Expression,
) -> Expression:
    recur = partial(opt_expr)

    match expr:
        case Int():
            return expr

        case Unit():
            return expr

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [Int(0), e2]:
                    return e2
                case [e1, Int(0)]:
                    return e1
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case [Int(i1), Add(Int(i2), e2)]:
                    return Add(Int(i1 + i2), e2)
                case [Add(Int(i1), e1), Add(Int(i2), e2)]:
                    return Add(Int(i1 + i2), Add(e1, e2))
                case [e1, Int() as e2]:
                    return Add(e2, e1)
                case [e1, e2]:  # pragma: no branch
                    return Add(e1, e2)

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case [e1, e2]:  # pragma: no branch
                    return Subtract(e1, e2)

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [Int(0), e2]:
                    return Int(0)
                case [e1, Int(0)]:
                    return Int(0)
                case [Int(1), e2]:
                    return e2
                case [e1, Int(1)]:
                    return e1
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case [Int(i1), Multiply(Int(i2), e2)]:
                    return Multiply(Int(i1 * i2), e2)
                case [Multiply(Int(i1), e1), Multiply(Int(i2), e2)]:
                    return Multiply(Int(i1 * i2), Multiply(e1, e2))
                case [e1, Int() as e2]:
                    return Multiply(e2, e1)
                case [e1, e2]:  # pragma: no branch
                    return Multiply(e1, e2)

        case Let(x, e1, e2):
            match recur(e2):
                case Var(y) if x == y:
                    return recur(e1)
                case e2:  # pragma: no branch
                    return Let(x, recur(e1), e2)

        case Var():
            return expr

        case Bool():
            return expr

        case If(e1, e2, e3):
            match recur(e1):
                case Bool(True):
                    return recur(e2)
                case Bool(False):
                    return recur(e3)
                case e1:  # pragma: no branch
                    return If(e1, recur(e2), recur(e3))

        case LessThan(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 < i2)
                case [e1, e2]:  # pragma: no branch
                    return LessThan(e1, e2)

        case EqualTo(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 == i2)
                case [Bool(b1), Bool(b2)]:
                    return Bool(b1 == b2)
                case [e1, e2]:  # pragma: no branch
                    return EqualTo(e1, e2)

        case GreaterThanOrEqualTo(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 >= i2)
                case [e1, e2]:  # pragma: no branch
                    return GreaterThanOrEqualTo(e1, e2)

        case Cell(e):
            return Cell(recur(e))

        case Get(cell):
            return Get(recur(cell))

        case Set(cell, value):
            return Set(recur(cell), recur(value))

        case Do(effect, value):
            return Do(recur(effect), recur(value))

        case While(c, body):
            new_c = recur(c)
            new_body = recur(body)
            if isinstance(new_c, Bool) and not new_c.value:
                return Unit()
            else:
                return While(new_c, new_body)

        case _:  # pragma: branch
            raise NotImplementedError()
