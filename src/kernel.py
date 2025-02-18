from dataclasses import dataclass
import typing


type Expression = typing.Union[
    # Int
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    # Var
    Let[Expression, Expression],
    Var,
    # If
    Bool,
    If[Expression, Expression, Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThanOrEqualTo[Expression],
    # Store
    Unit,
    Tuple[Expression],
    Get[Expression],
    Set[Expression],
    Do[Expression, Expression],
    # While
    While[Expression, Expression],
]


@dataclass(frozen=True)
class Int:
    value: int


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
class Let[Value, Name]:
    name: str
    value: Value
    body: Name


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Bool:
    value: bool


@dataclass(frozen=True)
class If[Condition, Consequent, Alternative]:
    condition: Condition
    consequent: Consequent
    alternative: Alternative


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
class Unit:
    pass


@dataclass(frozen=True)
class Tuple[Operand]:
    components: typing.Sequence[Operand]


@dataclass(frozen=True)
class Get[Operand]:
    tuple: Operand
    index: int


@dataclass(frozen=True)
class Set[Operand]:
    tuple: Operand
    index: int
    value: Operand


@dataclass(frozen=True)
class Do[Effect, Value]:
    effect: Effect
    second: Value


@dataclass(frozen=True)
class While[Condition, Body]:
    condition: Condition
    body: Body


@dataclass(frozen=True)
class Program:
    parameters: typing.Sequence[str]
    body: Expression
