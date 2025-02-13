from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Union


type Expression = Union[
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    Not,
    And,
    Or,
    If,
    LessThan,
    LessThanOrEqualTo,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqualTo,
]


@dataclass(frozen=True)
class Int:
    value: int


@dataclass(frozen=True)
class Add:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class Subtract:
    operands: Annotated[Sequence[Expression], "non-empty"]


@dataclass(frozen=True)
class Multiply:
    operands: Sequence[Expression]


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
class Not:
    operand: Expression


@dataclass(frozen=True)
class And:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class Or:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class If:
    condition: Expression
    consequent: Expression
    alternative: Expression


@dataclass(frozen=True)
class LessThan:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class LessThanOrEqualTo:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class EqualTo:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class GreaterThan:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class GreaterThanOrEqualTo:
    operands: Sequence[Expression]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
