from collections.abc import Callable, Mapping
from functools import partial
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var


type Environment = Mapping[str, str]


def uniqify(
    program: Program,
    fresh: Callable[[str], str],
) -> Program:
    local = {x: fresh(x) for x in program.parameters}
    return Program(
        parameters=list(local.values()),
        body=uniqify_expr(program.body, local, fresh),
    )


def uniqify_expr(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
) -> Expression:
    recur = partial(uniqify_expr, env=env, fresh=fresh)

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
            y = fresh(x)
            return Let(y, recur(e1), recur(e2, env={**env, x: y}))

        case Var(x):  # pragma: no branch
            return Var(env[x])
