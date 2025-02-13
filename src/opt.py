from functools import partial
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var, Bool, If, Compare


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

        case Compare(operator, e1, e2):  # pragma: no branch
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    match operator:
                        case "<":
                            return Bool(i1 < i2)
                        case "==":
                            return Bool(i1 == i2)
                        case ">=":  # pragma: no branch
                            return Bool(i1 >= i2)

                case [e1, e2]:  # pragma: no branch
                    return Compare(operator, e1, e2)
