from collections.abc import Sequence, Mapping
from functools import partial
from typing import Union
from kernel import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
)


type Value = Union[Int, Bool]
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

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case [_, _]:  # pragma: no cover
                    raise ValueError()

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case Let(x, e1, e2):
            return recur(e2, env={**env, x: recur(e1)})

        case Var(x):
            if x not in env:
                raise KeyError(f"Undefined variable: {x}")
            return env[x]

        # New cases For Bool and Conditionals :

        case Bool():
            return expr
        case If(c, t, f):
            cond_val = recur(c)
            if isinstance(cond_val, Bool):
                return recur(t) if cond_val.value else recur(f)
            else:  # pragma: no cover
                raise ValueError()

        case LessThan(x, y):
            v1 = recur(x)
            v2 = recur(y)
            if isinstance(v1, Int) and isinstance(v2, Int):
                return Bool(v1.value < v2.value)
            else:  # pragma: no cover
                raise ValueError()

        case EqualTo(x, y):
            v1 = recur(x)
            v2 = recur(y)
            return Bool(v1 == v2)

        case GreaterThanOrEqualTo(x, y):
            v1 = recur(x)
            v2 = recur(y)
            if isinstance(v1, Int) and isinstance(v2, Int):
                return Bool(v1.value >= v2.value)
            else:  # pragma: no cover
                raise ValueError()

        case _:
            raise NotImplementedError()
