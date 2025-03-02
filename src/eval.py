from collections.abc import Sequence, Mapping
from dataclasses import dataclass
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
    Unit,
    Cell,
    Get,
    Set,
    Do,
    While,
)
from store import Store


@dataclass(frozen=True)
class Location:
    value: int


type Value = Union[Int, Bool, Unit, Location]

type Environment = Mapping[str, Value]


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

        case Unit():
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
            if x not in env:
                raise KeyError(f"Undefined variable: {x}")
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

        case Cell(value):
            base = store.malloc(1)
            store[(base, 0)] = recur(value)
            return Location(base)

        case Get(cell):
            cell_val = recur(cell)
            if isinstance(cell_val, Location):
                return store[(cell_val.value, 0)]
            else:
                raise ValueError("Expected a Location")

        case Set(cell, new_value):
            cell_val = recur(cell)
            if isinstance(cell_val, Location):
                store[(cell_val.value, 0)] = recur(new_value)
            else:
                raise ValueError("Expected a Location")
            return Unit()

        case Do(effect, value):
            recur(effect)
            return recur(value)

        case While(condition, body):
            while True:
                cond_val = recur(condition)
                if isinstance(cond_val, Bool):
                    if not cond_val.value:
                        return Unit()
                    recur(body)
                else:
                    raise ValueError("While condition must evaluate to Bool")

        case _:  # pragma: no branch
            raise NotImplementedError()
