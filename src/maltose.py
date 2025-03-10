from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from lactose import (
    Int,
    Var,
    Bool,
    Unit,
    Add,
    Subtract,
    Multiply,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Lambda,
    Copy,
    Set,
    Let,
    If,
    Apply,
    Halt,
)

type Atom = Union[
    Int,
    Var,
    Bool,
    Unit,
]

type Expression = Union[
    Add[Atom],
    Subtract[Atom],
    Multiply[Atom],
    LessThan[Atom],
    EqualTo[Atom],
    GreaterThanOrEqualTo[Atom],
    Tuple[Atom],
    Get[Atom],
    Set[Atom],
    Lambda[Statement],
    Copy[Atom],
]


type Statement = Union[
    Let[Expression, Statement],
    If[Atom, Statement, Statement],
    Apply[Atom],
    Halt[Atom],
]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Statement
