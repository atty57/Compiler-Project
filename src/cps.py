from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from monadic import (
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
    Block,
]


type Statement = Union[
    Assign,
    Set[Atom],
]

type Tail = Union[
    Do[Statement, Tail],
    Return,
    Jump,
    If[Atom, Jump, Jump],
]


@dataclass(frozen=True)
class Block:
    body: Tail


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
