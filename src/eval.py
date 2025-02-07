from collections.abc import Mapping
from functools import partial
from kernel import Expression, Int, Add, Subtract, Multiply, Let, Var

type Value = int
type Environment = Mapping[str, Value]


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
            raise NotImplementedError()

        case Var(x):
            raise NotImplementedError()
