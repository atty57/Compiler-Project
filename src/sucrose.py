from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union, Sequence
from glucose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    If,
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    Lambda,
    Apply,
)

type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Div[Expression],
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
    Lambda[Expression],
    Apply[Expression],
    #
    Assign[Expression],
]


@dataclass(frozen=True)
class Assign[Value]:
    name: str
    value: Value


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
