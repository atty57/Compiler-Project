from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from kernel import (
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
    Let[Expression, Expression],
    If[Expression, Expression, Expression],
    LessThan[Atom],
    EqualTo[Atom],
    GreaterThanOrEqualTo[Atom],
    Cell[Atom],
    Get[Atom],
    Set[Atom],
    Do[Expression, Expression],
    While[Expression, Expression],
]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
