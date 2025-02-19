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
    Block[Tail],
]


type Statement = Union[
    Assign,
    Set[Atom],
    Apply[Atom],
]

type Tail = Union[
    Do[Statement, Tail],
    Return,
    Jump,
    If[Atom, Jump, Jump],
]


@dataclass(frozen=True)
class Block[Body]:
    body: Body


@dataclass(frozen=True)
class Assign:
    name: str
    value: Expression


@dataclass(frozen=True)
class Jump:
    target: str


@dataclass(frozen=True)
class Return:
    value: Expression


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Tail
