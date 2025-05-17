from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union, Any as TypingAny
from sucrose import (
    Int,
    Var,
    Bool,
    If,
    Unit,
    Lambda,
    Apply,
    Assign,
)

type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Div[Expression],
    Let[Expression, Expression],
    LetStar[Expression, Expression],
    LetRec[Expression, Expression],
    Var,
    Bool,
    Not[Expression],
    And[Expression],
    Or[Expression],
    If[Expression, Expression, Expression],
    Cond[Expression, Expression, Expression],
    LessThanOrEqualTo[Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThan[Expression],
    GreaterThanOrEqualTo[Expression],
    Unit,
    Cell[Expression],
    Get[Expression],
    Set[Expression],
    Begin[Expression],
    While[Expression, Expression],
    Lambda[Expression],
    Apply[Expression],
    Assign[Expression],
]


@dataclass(frozen=True)
class Add[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Subtract[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Multiply[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Div[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Let[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class LetStar[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class LetRec[Value, Body]:
    bindings: Sequence[tuple[str, Value]]
    body: Body


@dataclass(frozen=True)
class Not[Operand]:
    operand: Operand


@dataclass(frozen=True)
class And[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Or[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Cond[Condition, Consequent, Default]:
    arms: Sequence[tuple[TypingAny, TypingAny]]
    default: TypingAny
    __match_args__ = ("arms", "default")


@dataclass(frozen=True)
class Do:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class LessThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LessThan[Operand]:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None

    @property
    def y(self):
        return self.operands[1] if len(self.operands) >= 2 else None


@dataclass(frozen=True)
class EqualTo[Operand]:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None

    @property
    def y(self):
        return self.operands[1] if len(self.operands) >= 2 else None


@dataclass(frozen=True)
class GreaterThan[Operand]:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None

    @property
    def y(self):
        return self.operands[1] if len(self.operands) >= 2 else None


@dataclass(frozen=True)
class GreaterThanOrEqualTo[Operand]:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None


@dataclass(frozen=True)
class Cell[Operand]:
    value: Operand


@dataclass(frozen=True)
class Get[Operand]:
    cell: Operand


@dataclass(frozen=True)
class Set[Operand]:
    cell: Operand
    value: Operand


@dataclass(frozen=True)
class Begin[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class While[Condition, Body]:
    condition: Condition
    body: Body


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression


@dataclass(frozen=True)
class Sum:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class Difference:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class Product:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class NonDescending:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class Ascending:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class Same:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class Descending:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class NonAscending:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class Match:
    expr: TypingAny
    arms: Sequence[tuple[TypingAny, TypingAny]]


@dataclass(frozen=True)
class PatternVar:
    name: str


@dataclass(frozen=True)
class PatternInt:
    value: int


@dataclass(frozen=True)
class PatternTrue:
    pass


@dataclass(frozen=True)
class PatternFalse:
    pass


@dataclass(frozen=True)
class PatternUnit:
    pass


@dataclass(frozen=True)
class PatternWildcard:
    pass


@dataclass(frozen=True)
class PatternCons:
    constructor: str
    patterns: Sequence[TypingAny]
