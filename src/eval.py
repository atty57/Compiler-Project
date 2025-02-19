from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from typing import Union
from glucose import (
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
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    While,
    Lambda,
    Apply,
)
from store import Store


type Value = Union[Int, Bool, Unit, Location, Closure]

type Environment = Mapping[str, Value]


@dataclass(frozen=True)
class Location:
    value: int


@dataclass(frozen=True)
class Closure:
    abs: Lambda[Expression]
    env: Environment


def eval(
    program: Program,
    arguments: Sequence[Int],
) -> Value:
    return eval_expr(
        expr=program.body,
        env={p: a for p, a in zip(program.parameters, arguments, strict=True)},
        store=Store(),
    )


def eval_expr(
    expr: Expression,
    env: Environment,
    store: Store[Value],
) -> Value:
    recur = partial(eval_expr, env=env, store=store)
    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case _:  # pragma: no cover
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

        case LessThan(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 < i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case EqualTo(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 == i2)
                case [Bool(b1), Bool(b2)]:
                    return Bool(b1 == b2)
                case _:  # pragma: no cover
                    raise ValueError()

        case GreaterThanOrEqualTo(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 >= i2)
                case _:  # pragma: no cover
                    raise ValueError()

        case Unit():
            return expr

        case Tuple(es):
            base = store.malloc(1)
            for i, e in enumerate(es):
                store[base, i] = recur(e)
            return Location(base)

        case Get(e1, i):
            match recur(e1):
                case Location(base):
                    return store[base, i]
                case _:  # pragma: no cover
                    raise ValueError()

        case Set(e1, i, e2):
            match recur(e1):
                case Location(base):
                    store[base, i] = recur(e2)
                    return Unit()
                case _:  # pragma: no cover
                    raise ValueError()

        case Do(e1, e2):
            recur(e1)
            return recur(e2)

        case While(e1, e2):
            while True:
                match recur(e1):
                    case Bool(True):
                        recur(e2)
                    case Bool(False):
                        break
                    case _:  # pragma: no cover
                        raise ValueError()
            return Unit()

        case Lambda():
            return Closure(expr, env)

        case Apply(callee, arguments):  # pragma: no branch
            match recur(callee):
                case Closure(Lambda(parameters, body), env):
                    return recur(
                        body,
                        env={
                            **env,
                            **{p: recur(a) for p, a in zip(parameters, arguments, strict=True)},
                        },
                    )
                case _:  # pragma: no cover
                    raise ValueError()
