from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from maltose import (
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
    Do,
    Lambda,
    Apply,
)

type Atom = Union[
    Int,
    Var,
    Bool,
    Unit,
]

type Expression = Union[
    Atom,
    Add[Atom],
    Subtract[Atom],
    Multiply[Atom],
    LessThan[Atom],
    EqualTo[Atom],
    GreaterThanOrEqualTo[Atom],
    Tuple[Atom],
    Get[Atom],
    Lambda[Tail],
    Apply[Atom],
]

type Statement = Union[
    Assign[Expression],
    Set[Atom],
    Apply[Atom],
    Block[Tail],
]

type Tail = Union[
    Do[Statement, Tail],
    Return[Expression],
    Jump,
    If[Atom, Jump, Jump],
]


@dataclass(frozen=True)
class Assign[Value]:
    name: str
    value: Value


@dataclass(frozen=True)
class Block[Body]:
    name: str
    body: Body


@dataclass(frozen=True)
class Jump:
    target: str


@dataclass(frozen=True)
class Return[Value]:
    value: Value


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Tail
