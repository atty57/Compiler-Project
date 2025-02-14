from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Union


type Expression = Union[
    Int,
    Var,
    Unary,
    Binary[Literal["+"]],
    Binary[Literal["-", "*", "<", "==", ">="]],
    Bool,
    Unit,
    Block,
]

type Statement = Union[
    Assign,
    Binary[Literal[":="]],
]

type Tail = Union[
    Seq,
    Jump,
    Branch,
    Return,
]


@dataclass(frozen=True)
class Assign:
    name: str
    value: Expression


@dataclass(frozen=True)
class Seq:
    statement: Statement
    next: Tail


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Unary:
    operator: Literal["cell", "^"]
    x: str


@dataclass(frozen=True)
class Binary[Operator]:
    operator: Operator
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
class Unit:
    pass


@dataclass(frozen=True)
class Block:
    body: Tail


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
    body: Tail
