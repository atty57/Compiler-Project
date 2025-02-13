from collections.abc import Callable, Mapping
from functools import partial
from kernel import Program, Expression, Int, Binary, Let, Var, Bool, If, Unit, While


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

        case Binary(operator, e1, e2):
            return Binary(operator, recur(e1), recur(e2))

        case Let(x, e1, e2):
            y = fresh(x)
            return Let(y, recur(e1), recur(e2, env={**env, x: y}))

        case Var(x):
            return Var(env[x])

        case Bool():
            return expr

        case If(e1, e2, e3):
            return If(recur(e1), recur(e2), recur(e3))

        case Unit():
            return expr

        case While(e1, e2):  # pragma: no branch
            return While(recur(e1), recur(e2))
