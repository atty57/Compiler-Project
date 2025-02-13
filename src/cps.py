from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Union


type Expression = Union[
    Int,
    Var,
    Binary,
    Bool,
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
class Binary:
    operator: Literal[
        "+",
        "-",
        "*",
        "<",
        "==",
        ">=",
    ]
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
