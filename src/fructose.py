from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Union
from sucrose import (
    Int,
    Let,
    Var,
    Bool,
    If,
    Unit,
    Tuple,
    Get,
    Set,
    While,
    Assign,
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
    LetStar[Expression, Expression],
    Not[Expression],
    All[Expression],
    Any[Expression],
    Bool,
    If[Expression, Expression, Expression],
    Cond[Expression, Expression, Expression],
    LessThanOrEqualTo[Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThan[Expression],
    GreaterThanOrEqualTo[Expression],
    Unit,
    Tuple[Expression],
    Get[Expression],
    Set[Expression],
    Do[Expression],
    While[Expression, Expression],
    Assign[Expression],
    Lambda[Expression],
    Apply[Expression],
    #
    Cell[Expression],
    CellGet[Expression],
    CellSet[Expression],
    Vector[Expression],
    VectorLength[Expression],
    VectorGet[Expression],
    VectorSet[Expression],
]


@dataclass(frozen=True)
class Add[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Subtract[Operand]:
    operands: Annotated[Sequence[Operand], "non-empty"]


@dataclass(frozen=True)
class Multiply[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LetStar[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class Not[Operand]:
    x: Operand


@dataclass(frozen=True)
class All[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Any[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Cond[Condition, Consequent, Default]:
    arms: Sequence[tuple[Condition, Consequent]]
    default: Default


@dataclass(frozen=True)
class LessThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LessThan[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class EqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class GreaterThan[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class GreaterThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Cell[Operand]:
    value: Operand


@dataclass(frozen=True)
class CellGet[Operand]:
    cell: Operand


@dataclass(frozen=True)
class CellSet[Operand]:
    cell: Operand
    value: Operand


@dataclass(frozen=True)
class Vector[Operand]:
    elements: Sequence[Operand]


@dataclass(frozen=True)
class VectorLength[Operand]:
    vector: Operand


@dataclass(frozen=True)
class VectorGet[Operand]:
    vector: Operand
    index: int


@dataclass(frozen=True)
class VectorSet[Operand]:
    vector: Operand
    index: int
    value: Operand


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression


@dataclass(frozen=True)
class Do[Operand]:
    operands: Sequence[Operand]
