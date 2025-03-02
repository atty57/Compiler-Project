from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Union, Any as TypingAny
from kernel import Int, Let, Var, Bool, If, Unit, Cell, Get, Set, While


type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Let[Expression, Expression],
    Var,
    LetStar[Expression, Expression],
    Bool,
    Not[Expression],
    All[Expression],
    TypingAny[Expression],
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
    Do[Expression],
    While[Expression, Expression],
]


@dataclass(frozen=True)
class Add[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Subtract[Operand]:
    operands: Annotated[Sequence[Operand], "non-empty"]


@dataclass(frozen=True)
class Multiply[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class Not[Operand]:
    x: Operand


@dataclass(frozen=True)
class All:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)

@dataclass(frozen=True)
class Any:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class AnyExpression:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class Cond:
    arms: Sequence[tuple[TypingAny, TypingAny]]
    default: TypingAny
    __match_args__ = ("arms", "default")


@dataclass(frozen=True)
class LetStar:
    bindings: Sequence[tuple[str, TypingAny]]
    body: TypingAny
    __match_args__ = ("bindings", "body")


@dataclass(frozen=True)
class Do:
    operands: Sequence[TypingAny]
    __match_args__ = ("operands",)


@dataclass(frozen=True)
class LessThanOrEqualTo[Operand]:
    operands: Sequence[Operand]


@dataclass(frozen=True)
class LessThan:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None

    @property
    def y(self):
        return self.operands[1] if len(self.operands) >= 2 else None


@dataclass(frozen=True)
class EqualTo:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None

    @property
    def y(self):
        return self.operands[1] if len(self.operands) >= 2 else None


@dataclass(frozen=True)
class GreaterThan:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None

    @property
    def y(self):
        return self.operands[1] if len(self.operands) >= 2 else None


@dataclass(frozen=True)
class GreaterThanOrEqualTo:
    operands: Sequence[TypingAny]
    __match_args__ = ("x", "y")

    @property
    def x(self):
        return self.operands[0] if len(self.operands) >= 1 else None

    @property
    def y(self):
        return self.operands[1] if len(self.operands) >= 2 else None


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
