from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Union


type Expression = Union[
    Int,
    Unary,
    Binary,
    Let,
    Var,
    Bool,
    If,
    Unit,
    While,
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Unary:
    operator: Literal["cell", "^"]
    x: str


@dataclass(frozen=True)
class Binary:
    operator: Literal["+", "-", "*", "<", "==", ">=", ":="]
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
class Bool:
    value: bool


@dataclass(frozen=True)
class If:
    condition: Expression
    consequent: Expression
    alternative: Expression


@dataclass(frozen=True)
class Unit:
    pass


@dataclass(frozen=True)
class While:
    condition: Expression
    body: Expression


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
