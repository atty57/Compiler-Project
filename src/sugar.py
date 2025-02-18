from collections.abc import Sequence
from dataclasses import dataclass
import typing
import kernel


type Expression = typing.Union[
    kernel.Int,
    kernel.Add[Expression],
    kernel.Subtract[Expression],
    kernel.Multiply[Expression],
    kernel.Let[Expression, Expression],
    kernel.Var,
    kernel.Bool,
    kernel.If[Expression, Expression, Expression],
    kernel.LessThan[Expression],
    kernel.EqualTo[Expression],
    kernel.GreaterThanOrEqualTo[Expression],
    kernel.Unit,
    kernel.Tuple[Expression],
    kernel.Get[Expression],
    kernel.Set[Expression],
    kernel.Do[Expression, Expression],
    kernel.While[Expression, Expression],
    #
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    LetStar[Expression, Expression],
    Not[Expression],
    All[Expression],
    Any[Expression],
    Cond[Expression, Expression, Expression],
    LessThanOrEqualTo[Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThan[Expression],
    GreaterThanOrEqualTo[Expression],
    Do[Expression],
]


@dataclass(frozen=True)
class Add[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Subtract[Operand]:
    operands: typing.Annotated[Sequence[Operand], "non-empty"]


@dataclass(frozen=True)
class Multiply[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LetStar[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class Not[Operand]:
    x: Operand


@dataclass(frozen=True)
class All[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Any[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Cond[Condition, Consequent, Default]:
    arms: Sequence[tuple[Condition, Consequent]]
    default: Default


@dataclass(frozen=True)
class LessThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LessThan[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class EqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class GreaterThan[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class GreaterThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Do[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression
