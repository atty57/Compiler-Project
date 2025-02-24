from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from lactose import (
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
    Apply,
    Assign,
    Return,
    Jump,
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
    Apply[Atom],
]


type Statement = Union[
    Assign[Expression],
    Set[Atom],
    Apply[Atom],
]

type Tail = Union[
    Do[Statement, Tail],
    Return[Expression],
    Jump,
    If[Atom, Jump, Jump],
]


@dataclass(frozen=True)
class Block:
    name: str
    body: Tail


@dataclass(frozen=True)
class Function:
    name: str
    parameters: Sequence[str]
    blocks: Sequence[Block]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Tail
    functions: Sequence[Function]
