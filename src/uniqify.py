from collections.abc import Callable, MutableMapping
from functools import partial
from glucose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
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
    Lambda,
    Apply,
)


type Environment = MutableMapping[str, str]


def uniqify(
    program: Program,
    fresh: Callable[[str], str],
) -> Program:
    local = {parameter: fresh(parameter) for parameter in program.parameters}
    return Program(
        parameters=list(local.values()),
        body=uniqify_expression(program.body, local, fresh),
    )


def uniqify_expression(
    expr: Expression,
    env: Environment,
    fresh: Callable[[str], str],
) -> Expression:
    recur = partial(uniqify_expression, env=env, fresh=fresh)

    match expr:
        case Int():
            return expr

        case Add(x, y):
            return Add(recur(x), recur(y))

        case Subtract(x, y):
            return Subtract(recur(x), recur(y))

        case Multiply(x, y):
            return Multiply(recur(x), recur(y))

        case Var(x):
            return Var(env[x])

        case Bool():
            return expr

        case If(condition, consequent, alternative):
            return If(recur(condition), recur(consequent), recur(alternative))

        case LessThan(x, y):
            return LessThan(recur(x), recur(y))

        case EqualTo(x, y):
            return EqualTo(recur(x), recur(y))

        case GreaterThanOrEqualTo(x, y):
            return GreaterThanOrEqualTo(recur(x), recur(y))

        case Unit():
            return expr

        case Tuple(components):
            return Tuple([recur(e) for e in components])

        case Get(tuple, index):
            return Get(recur(tuple), recur(index))

        case Set(tuple, index, value):
            return Set(recur(tuple), recur(index), recur(value))

        case Lambda(params, body):
            old_env = dict(env)
            new_params: list[str] = []
            for p in params:
                new_p = fresh(p)
                new_params.append(new_p)
                env[p] = new_p
            new_body = uniqify_expression(body, env, fresh)
            env.clear()
            env.update(old_env)
            return Lambda(new_params, new_body)

        case Apply(callee, arguments):
            new_callee = recur(callee)
            new_args = [recur(a) for a in arguments]
            return Apply(new_callee, new_args)

        case _:
            raise NotImplementedError(f"uniqify_expression not implemented for {expr}")
