from functools import partial
from constant_folding import constant_fold
from glucose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Div,
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


class CompileError(Exception):
    pass


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

        case Div(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    if i2 == 0:
                        raise CompileError("division by zero at compile time")
                    return Int(i1 // i2)
                case [e1, e2]:  # pragma: no branch
                    return Div(e1, e2)

        case Let(x, value, body):
            match recur(body):
                case Var(y) if x == y:
                    return recur(value)
                case body:  # pragma: no branch
                    return Let(x, recur(value), body)

        case Var():
            return expr

        case Bool():
            return expr

        case If(condition, consequent, alternative):
            match recur(condition):
                case Bool(True):
                    return recur(consequent)
                case Bool(False):
                    return recur(alternative)
                case condition:  # pragma: no branch
                    return If(condition, recur(consequent), recur(alternative))

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

        case Unit():
            return expr

        case Tuple(components):
            return Tuple([recur(component) for component in components])

        case Get(tuple, index):
            match recur(tuple), recur(index):
                case [Tuple(components), Int(i)] if i in range(len(components)):
                    return components[i]
                case tuple, index:  # pragma: no branch
                    return Get(tuple, index)

        case Set(tuple, index, value):
            return Set(recur(tuple), index, recur(value))

        case Do(effect, value):
            return Do(recur(effect), recur(value))

        case Lambda(parameters, body):
            return Lambda(parameters, recur(body))

        case Apply(callee, arguments):  # pragma no branch
            return Apply(recur(callee), [recur(argument) for argument in arguments])
