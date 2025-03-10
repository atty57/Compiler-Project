from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from maltose import (
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
    Lambda[Expression],
    Apply[Expression],
]


@dataclass(frozen=True)
class Do[Effect, Value]:
    effect: Effect
    value: Value


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
