from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from monadic import (
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
    Set[Atom],
    Block,
]

type Statement = Union[
    Let[Expression, Statement],
    Return,
    Jump,
    If[Atom, Jump, Jump],
]


@dataclass(frozen=True)
class Block:
    body: Statement


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
    body: Statement
