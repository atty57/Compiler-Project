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
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Cell,
    Get,
    Set,
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
    Cell[Atom],
    Get[Atom],
    Block,
]

type Statement = Union[
    Assign,
    Set[Atom],
]


type Tail = Union[
    Seq,
    Jump,
    Branch,
    Return,
]


@dataclass(frozen=True)
class Block:
    body: Tail


@dataclass(frozen=True)
class Assign:
    name: str
    value: Expression


@dataclass(frozen=True)
class Seq:
    statement: Statement
    next: Tail


@dataclass(frozen=True)
class Jump:
    target: str


@dataclass(frozen=True)
class Branch:
    condition: Var
    then: Jump
    otherwise: Jump


@dataclass(frozen=True)
class Return:
    value: Expression


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Tail
