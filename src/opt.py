from functools import partial
from kernel import Program, Expression, Int, Binary, Let, Var, Bool, If, Unit, While


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

        case Binary(operator, e1, e2):
            match operator:
                case "+":
                    match recur(e1), recur(e2):
                        case [Int(0), e2]:
                            return e2
                        case [e1, Int(0)]:
                            return e1
                        case [Int(i1), Int(i2)]:
                            return Int(i1 + i2)
                        case [Int(i1), Binary("+", Int(i2), e2)]:
                            return Binary("+", Int(i1 + i2), e2)
                        case [Binary("+", Int(i1), e1), Binary("+", Int(i2), e2)]:
                            return Binary("+", Int(i1 + i2), Binary("+", e1, e2))
                        case [e1, Int() as e2]:
                            return Binary("+", e2, e1)
                        case [e1, e2]:  # pragma: no branch
                            return Binary("+", e1, e2)

                case "-":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Int(i1 - i2)
                        case [e1, e2]:  # pragma: no branch
                            return Binary("-", e1, e2)

                case "*":
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
                        case [Int(i1), Binary("*", Int(i2), e2)]:
                            return Binary("*", Int(i1 * i2), e2)
                        case [Binary("*", Int(i1), e1), Binary("*", Int(i2), e2)]:
                            return Binary("*", Int(i1 * i2), Binary("*", e1, e2))
                        case [e1, Int() as e2]:
                            return Binary("*", e2, e1)
                        case [e1, e2]:  # pragma: no branch
                            return Binary("*", e1, e2)

                case "<":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Bool(i1 < i2)
                        case [e1, e2]:  # pragma: no branch
                            return Binary("<", e1, e2)

                case "==":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Bool(i1 == i2)
                        case [Bool(b1), Bool(b2)]:
                            return Bool(b1 == b2)
                        case [e1, e2]:  # pragma: no branch
                            return Binary("==", e1, e2)

                case ">=":  # pragma: no branch
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Bool(i1 >= i2)
                        case [e1, e2]:  # pragma: no branch
                            return Binary(">=", e1, e2)

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

        case Unit():
            return expr

        case While(e1, e2):  # pragma no branch
            match recur(e1):
                case Bool(False):
                    return Unit()
                case e1:
                    return While(e1, recur(e2))
