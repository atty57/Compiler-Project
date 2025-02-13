from collections.abc import Sequence, Mapping
from functools import partial
from typing import Union
from kernel import Program, Expression, Int, Binary, Let, Var, Bool, If, Unit, While


type Value = Union[
    Int,
    Bool,
    Unit,
]

type Environment = Mapping[str, Value]


def eval(
    program: Program,
    arguments: Sequence[Value],
) -> Value:
    env: Environment = {p: a for p, a in zip(program.parameters, arguments, strict=True)}
    return eval_expr(program.body, env)


def eval_expr(
    expr: Expression,
    env: Environment,
) -> Value:
    recur = partial(eval_expr, env=env)
    match expr:
        case Int():
            return expr

        case Binary(operator, e1, e2):
            match operator:
                case "+":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Int(i1 + i2)
                        case _:  # pragma: no cover
                            raise ValueError()

                case "-":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Int(i1 - i2)
                        case _:  # pragma: no cover
                            raise ValueError()

                case "*":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Int(i1 * i2)
                        case _:  # pragma: no cover
                            raise ValueError()

                case "<":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Bool(i1 < i2)
                        case _:  # pragma: no cover
                            raise ValueError()

                case "==":
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Bool(i1 == i2)
                        case [Bool(b1), Bool(b2)]:
                            return Bool(b1 == b2)
                        case _:  # pragma: no cover
                            raise ValueError()

                case ">=":  # pragma: no branch
                    match recur(e1), recur(e2):
                        case [Int(i1), Int(i2)]:
                            return Bool(i1 >= i2)
                        case _:  # pragma: no cover
                            raise ValueError()

        case Let(x, e1, e2):
            return recur(e2, env={**env, x: recur(e1)})

        case Var(x):
            return env[x]

        case Bool():
            return expr

        case If(e1, e2, e3):
            match recur(e1):
                case Bool(True):
                    return recur(e2)
                case Bool(False):
                    return recur(e3)
                case _:  # pragma: no cover
                    raise ValueError()

        case Unit():
            return expr

        case While(e1, e2):  # pragma: no branch
            while True:
                match recur(e1):
                    case Bool(False):
                        break
                    case Bool(True):
                        recur(e2)
                    case _:  # pragma: no cover
                        raise ValueError()

            return Unit()
