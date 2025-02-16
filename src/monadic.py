from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from kernel import Int, Add, Subtract, Multiply, Let, Var, Bool, If, LessThan, EqualTo, GreaterThanOrEqualTo

type Expression = Union[
    Int,
    Add[str],
    Subtract[str],
    Multiply[str],
    Let[Expression, Expression],
    Var,
    Bool,
    If[Expression, Expression, Expression],
    LessThan[str],
    EqualTo[str],
    GreaterThanOrEqualTo[str],
]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
