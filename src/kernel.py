from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Union


type Expression = Union[
    Int,
    Binary,
    Let,
    Var,
    Bool,
    If,
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Binary:
    operator: Literal[
        "+",
        "-",
        "*",
        "<",
        "==",
        ">=",
    ]
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
class Program:
    parameters: Sequence[str]
    body: Expression
