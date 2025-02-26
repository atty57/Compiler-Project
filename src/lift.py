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
    Assign,
    Do,
    Return,
    Jump,
    If,
)
import cellulose


def lift_tail(tail: lactose.Tail) -> cellulose.Tail:
    match tail:
        case Do(stmt, next):
            pass

        case Return(value):
            pass

        case Jump(target):
            pass

        case If(condition, Jump(then), Jump(otherwise)):
            pass


def left_statement(statement: lactose.Statement) -> None:
    match statement:
        case Assign(name, value):
            pass
        case Set():
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
            | Apply()
        ):
            return expr, [], []

        case Lambda(xs, body):
            pass
