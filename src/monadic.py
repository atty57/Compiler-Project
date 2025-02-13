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
    If,
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Add:
    x: str
    y: str


@dataclass(frozen=True)
class Subtract:
    x: str
    y: str


@dataclass(frozen=True)
class Multiply:
    x: str
    y: str


@dataclass(frozen=True)
class Let:
    name: str
    value: Expression
    body: Expression


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class If:
    condition: Expression
    consequent: Expression
    alternative: Expression


@dataclass(frozen=True)
class Compare:
    operator: Literal[
        "<=",
        "<",
        "==",
        "!=",
        ">",
        ">=",
    ]
    x: str
    y: str


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
