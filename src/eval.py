from collections.abc import Sequence, Mapping
from functools import partial
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var

type Value = int
type Environment = Mapping[str, Value]


def eval(
    program: Program,
    arguments: Sequence[Value],
) -> Value:
    env: Environment = dict(zip(program.parameters, arguments)) # Bind parameters to arguments
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

        case Var(x):  # pragma: no branch
            if x not in env:
                raise KeyError(f"Undefined variable: {x}")
            return env[x]