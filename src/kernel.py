from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Union


type Expression = Union[
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    Compare,
    Unit,
    Cell,
    CellGet,
    CellSet,
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Add:
    x: Expression
    y: Expression


@dataclass(frozen=True)
class Subtract:
    x: Expression
    y: Expression


@dataclass(frozen=True)
class Multiply:
    x: Expression
    y: Expression


@dataclass(frozen=True)
class Let:
    name: str
    value: Expression
    body: Expression


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Bool:
    value: bool


@dataclass(frozen=True)
class If:
    condition: Expression
    consequent: Expression
    alternative: Expression


@dataclass(frozen=True)
class Compare:
    operator: Literal[
        "<",
        "==",
        ">=",
    ]
    x: Expression
    y: Expression


@dataclass(frozen=True)
class Unit:
    pass


@dataclass(frozen=True)
class Cell:
    value: Expression


@dataclass(frozen=True)
class CellGet:
    cell: Expression


@dataclass(frozen=True)
class CellSet:
    cell: Expression
    value: Expression


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
