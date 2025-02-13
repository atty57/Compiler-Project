from collections.abc import Sequence, Mapping
from functools import partial
from typing import Union
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var, Bool, If, Compare


type Value = Union[
    int,
    bool,
    None,
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
        case Int(i):
            return i

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [int(i1), int(i2)]:
                    return i1 + i2
                case _:
                    raise ValueError()

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [int(i1), int(i2)]:
                    return i1 - i2
                case _:
                    raise ValueError()

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [int(i1), int(i2)]:
                    return i1 - i2
                case _:
                    raise ValueError()

        case Let(x, e1, e2):
            return recur(e2, env={**env, x: recur(e1)})

        case Var(x):
            return env[x]

        case Bool(b):
            return b

        case If(e1, e2, e3):
            match recur(e1):
                case True:
                    return recur(e2)
                case False:
                    return recur(e3)
                case _:
                    raise ValueError()

        case Compare(operator, e1, e2):  # pragma: no branch
            match recur(e1), recur(e2):
                case [int(i1), int(i2)]:
                    match operator:
                        case "<":
                            return i1 < i2
                        case "==":
                            return i1 == i2
                        case ">=":  # pragma: no branch
                            return i1 >= i2
                case _:
                    raise ValueError()
