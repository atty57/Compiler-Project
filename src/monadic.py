from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from kernel import Int, Add, Subtract, Multiply, Let, Var, Bool, If, LessThan, EqualTo, GreaterThanOrEqualTo

type Atom = Union[
    Int,
    Var,
    Bool,
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
]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
