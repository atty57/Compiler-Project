from collections.abc import Sequence
from functools import partial
import lactose
from lactose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Var,
    Bool,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Tuple,
    Get,
    Set,
    Lambda,
    Apply,
    Block,
    Do,
    Return,
    Jump,
    If,
)
import cellulose


def lift_tail(tail: lactose.Tail) -> None:
    match tail:
        case Do(stmt, next):
            pass

        case Return(value):
            pass

        case Jump(target):
            pass

        case If(condition, Jump(then), Jump(otherwise)):
            pass


def lift_expr(
    expr: lactose.Expression,
) -> tuple[cellulose.Expression, Sequence[cellulose.Function], Sequence[cellulose.Block]]:
    match expr:
        case (
            Int()
            | Add()
            | Subtract()
            | Multiply()
            | Var()
            | Bool()
            | Unit()
            | LessThan()
            | EqualTo()
            | GreaterThanOrEqualTo()
            | Tuple()
            | Get()
            | Set()
            | Apply()
        ):
            return expr, [], []

        case Lambda(xs, body):
            pass

        case Block(body):
            pass
