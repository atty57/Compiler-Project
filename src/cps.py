from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Union


type Expression = Union[
    Int,
    Add,
    Subtract,
    Multiply,
    Var,
    Bool,
    Compare,
    Block,
]

type Statement = Union[
    Let,
    Jump,
    Branch,
    Return,
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
    body: Statement


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Bool:
    value: bool


@dataclass(frozen=True)
class Compare:
    operator: Literal[
        "<",
        "==",
        ">=",
    ]
    x: str
    y: str


@dataclass(frozen=True)
class Block:
    body: Statement


@dataclass(frozen=True)
class Jump:
    target: str


@dataclass(frozen=True)
class Branch:
    condition: str
    then: Jump
    otherwise: Jump


@dataclass(frozen=True)
class Return:
    value: Expression


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Statement
