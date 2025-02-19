from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from glucose import (
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
    Tuple,
    Get,
    Set,
    Do,
    While,
    Lambda,
    Apply,
)


type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Let[Expression, Expression],
    Var,
    Bool,
    If[Expression, Expression, Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThanOrEqualTo[Expression],
    Unit,
    Tuple[Expression],
    Get[Expression],
    Set[Expression],
    Do[Expression, Expression],
    While[Expression, Expression],
    Assign[Expression],
    Lambda[Expression],
    Apply[Expression],
]


@dataclass(frozen=True)
class Assign[Value]:
    name: str
    value: Value


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
