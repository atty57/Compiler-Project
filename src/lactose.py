from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Union

type Atom = Union[
    Int,
    Var,
    Bool,
    Unit,
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Bool:
    value: bool


@dataclass(frozen=True)
class Unit:
    pass


type Expression = Union[
    Add[Atom],
    Subtract[Atom],
    Multiply[Atom],
    Div[Atom],
    LessThan[Atom],
    EqualTo[Atom],
    GreaterThanOrEqualTo[Atom],
    Tuple[Atom],
    Get[Atom],
    Set[Atom],
    Copy[Atom],
    Global,
]


@dataclass(frozen=True)
class Add[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Subtract[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Multiply[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Div[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class LessThan[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class EqualTo[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class GreaterThanOrEqualTo[Operand]:
    x: Operand
    y: Operand


@dataclass(frozen=True)
class Tuple[Operand]:
    components: Sequence[Operand]


@dataclass(frozen=True)
class Get[Operand]:
    tuple: Operand
    index: Operand


@dataclass(frozen=True)
class Set[Operand]:
    tuple: Operand
    index: Operand
    value: Operand


@dataclass(frozen=True)
class Lambda[Body]:
    parameters: Sequence[str]
    body: Body


@dataclass(frozen=True)
class Global:
    name: str


@dataclass(frozen=True)
class Copy[Value]:
    value: Value


type Statement = Union[
    Let[Expression, Statement],
    If[Atom, Statement, Statement],
    Apply[Atom],
    Halt[Atom],
]


@dataclass(frozen=True)
class Let[Value, Body]:
    name: str
    value: Value
    body: Body


@dataclass(frozen=True)
class If[Condition, Consequent, Alternative]:
    condition: Condition
    consequent: Consequent
    alternative: Alternative


@dataclass(frozen=True)
class Apply[Operand]:
    callee: Operand
    arguments: Sequence[Operand]


@dataclass(frozen=True)
class Halt[Value]:
    value: Value


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Statement
    functions: Mapping[str, Lambda[Statement]]
