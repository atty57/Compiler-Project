from dataclasses import dataclass
from functools import partial
import typing
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
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    While,
)
from store import Store


@dataclass(frozen=True)
class Location:
    value: int


type Value = typing.Union[Int, Bool, Unit, Location]

type Environment = typing.Mapping[str, Value]


def eval(
    program: Program,
    arguments: typing.Sequence[Value],
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

        case While(e1, e2):  # pragma: no branch
            while True:
                match recur(e1):
                    case Bool(True):
                        recur(e2)
                    case Bool(False):
                        break
                    case _:  # pragma: no cover
                        raise ValueError()
            return Unit()
