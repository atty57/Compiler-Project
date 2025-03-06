from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from functools import partial
from itertools import count
from typing import Union
from maltose import (
    Program,
    Atom,
    Int,
    Var,
    Bool,
    Unit,
    Expression,
    Add,
    Subtract,
    Multiply,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Lambda,
    Copy,
    Statement,
    Let,
    If,
    Apply,
    Halt,
)

type Value = Union[
    Int,
    Bool,
    Unit,
    Location,
    Closure,
]

type Environment = Mapping[str, Value]
type Store = Mapping[Location, list[Value]]


@dataclass(frozen=True)
class Location:
    value: int


@dataclass(frozen=True)
class Closure:
    abs: Lambda[Statement]
    env: Environment


def eval(
    program: Program,
    arguments: Sequence[Int],
) -> tuple[Value, Store]:
    return eval_statement(
        statement=program.body,
        environment={p: a for p, a in zip(program.parameters, arguments, strict=True)},
        store={},
        locations=map(lambda i: Location(i), count(0)),
    )


def eval_statement(
    statement: Statement,
    environment: Environment,
    store: Store,
    locations: Iterator[Location],
) -> tuple[Value, Store]:
    atom = partial(eval_atom, environment=environment)
    expr = partial(eval_expression, environment=environment, store=store, locations=locations)
    recur = partial(eval_statement, environment=environment, store=store, locations=locations)

    match statement:
        case Let(name, value, body):
            value, s1 = expr(value)
            return recur(body, environment={**environment, name: value}, store=s1)

        case If(condition, then, otherwise):
            match atom(condition):
                case Bool(True):
                    return recur(then)
                case Bool(False):
                    return recur(otherwise)
                case _:  # pragma: no cover
                    raise ValueError()

        case Apply(callee, arguments):
            match atom(callee):
                case Closure(Lambda(parameters, body), environment):
                    return recur(
                        body,
                        environment={
                            **environment,
                            **{p: atom(a) for p, a in zip(parameters, arguments, strict=True)},
                        },
                    )
                case _:  # pragma: no cover
                    raise ValueError()

        case Halt(value):  # pragma: no branch
            return atom(value), store


def eval_expression(
    expression: Expression,
    environment: Environment,
    store: Store,
    locations: Iterator[Location],
) -> tuple[Value, Store]:
    atom = partial(eval_atom, environment=environment)

    match expression:
        case Add(e1, e2):
            match atom(e1), atom(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2), store
                case _:  # pragma: no cover
                    raise ValueError()

        case Subtract(e1, e2):
            match atom(e1), atom(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2), store
                case _:  # pragma: no cover
                    raise ValueError()

        case Multiply(e1, e2):
            match atom(e1), atom(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2), store
                case _:  # pragma: no cover
                    raise ValueError()

        case LessThan(e1, e2):
            match atom(e1), atom(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 < i2), store
                case _:  # pragma: no cover
                    raise ValueError()

        case EqualTo(e1, e2):
            match atom(e1), atom(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 == i2), store
                case [Bool(b1), Bool(b2)]:
                    return Bool(b1 == b2), store
                case _:  # pragma: no cover
                    raise ValueError()

        case GreaterThanOrEqualTo(e1, e2):
            match atom(e1), atom(e2):
                case [Int(i1), Int(i2)]:
                    return Bool(i1 >= i2), store
                case _:  # pragma: no cover
                    raise ValueError()

        case Tuple(components):
            location = next(locations)
            return location, {**store, location: [atom(component) for component in components]}

        case Get(tuple, index):
            match atom(tuple), atom(index):
                case [Location() as location, Int(i)]:
                    return store[location][i], store
                case _:  # pragma: no cover
                    raise ValueError()

        case Set(tuple, index, value):
            match atom(tuple), atom(index):
                case [Location() as location, Int(i)]:
                    store[location][i] = atom(value)
                    return Unit(), store
                case _:  # pragma: no cover
                    raise ValueError()

        case Lambda():
            return Closure(expression, environment), store

        case Copy(value):  # pragma: no branch
            return atom(value), store


def eval_atom(
    atom: Atom,
    environment: Environment,
) -> Value:
    match atom:
        case Int():
            return atom
        case Var(name):
            return environment[name]
        case Bool():
            return atom
        case Unit():  # pragma: no branch
            return atom
