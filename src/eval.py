from collections.abc import Sequence, Mapping
from functools import partial
from typing import Union
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var, Bool, If, Compare


type Value = Union[int, bool]
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
            return recur(e1) + recur(e2)

        case Subtract(e1, e2):
            return recur(e1) - recur(e2)

        case Multiply(e1, e2):
            return recur(e1) * recur(e2)

        case Let(x, e1, e2):
            return recur(e2, env={**env, x: recur(e1)})

        case Var(x):
            return env[x]

        case Bool(b):
            return b

        case If(e1, e2, e3):
            return recur(e2) if recur(e1) else recur(e3)

        case Compare(operator, e1, e2):  # pragma: no branch
            match operator:
                case "<":
                    return recur(e1) < recur(e2)
                case "==":
                    return recur(e1) == recur(e2)
                case ">=":  # pragma: no branch
                    return recur(e1) >= recur(e2)
