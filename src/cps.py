from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from monadic import Int, Add, Subtract, Multiply, Var, Bool, LessThan, EqualTo, GreaterThanOrEqualTo

type Expression = Union[
    Int,
    Add[str],
    Subtract[str],
    Multiply[str],
    Var,
    Bool,
    LessThan[str],
    EqualTo[str],
    GreaterThanOrEqualTo[str],
    Block,
]

type Statement = Assign


type Tail = Union[
    Seq,
    Jump,
    Branch,
    Return,
]


@dataclass(frozen=True)
class Block:
    body: Tail


@dataclass(frozen=True)
class Assign:
    name: str
    value: Expression


@dataclass(frozen=True)
class Seq:
    statement: Statement
    next: Tail


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
