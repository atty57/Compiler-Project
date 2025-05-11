from typing import Mapping
from glucose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Div,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Do,
    Lambda,
    Apply,
    Unit,
)


class CompileError(Exception):
    """Raised on a compile-time division by zero."""

    pass


def constant_fold(program: Program) -> Program:
    """Walk the AST, replacing any Add/Subtract/Multiply/Div of two Ints with a single Int."""
    return Program(program.parameters, _fold_expr(program.body))


def _fold_expr(expr: Expression) -> Expression:
    match expr:
        case Add(x, y):
            x2, y2 = _fold_expr(x), _fold_expr(y)
            if isinstance(x2, Int) and isinstance(y2, Int):
                return Int(x2.value + y2.value)
            # x + 0  or 0 + x
            if isinstance(x2, Int) and x2.value == 0:
                return y2
            if isinstance(y2, Int) and y2.value == 0:
                return x2
            return Add(x2, y2)

        case Subtract(x, y):
            x2, y2 = _fold_expr(x), _fold_expr(y)
            if isinstance(x2, Int) and isinstance(y2, Int):
                return Int(x2.value - y2.value)
            # x - 0
            if isinstance(y2, Int) and y2.value == 0:
                return x2
            return Subtract(x2, y2)

        case Multiply(x, y):
            x2, y2 = _fold_expr(x), _fold_expr(y)
            if isinstance(x2, Int) and isinstance(y2, Int):
                return Int(x2.value * y2.value)
            # x * 1 or 1 * x
            if isinstance(x2, Int) and x2.value == 1:
                return y2
            if isinstance(y2, Int) and y2.value == 1:
                return x2
            # x * 0 or 0 * x
            if (isinstance(x2, Int) and x2.value == 0) or (isinstance(y2, Int) and y2.value == 0):
                return Int(0)
            return Multiply(x2, y2)

        case Div(x, y):
            x2, y2 = _fold_expr(x), _fold_expr(y)
            if isinstance(x2, Int) and isinstance(y2, Int):
                if y2.value == 0:
                    raise CompileError("division by zero at compile time")
                return Int(x2.value // y2.value)
            # x / 1
            if isinstance(y2, Int) and y2.value == 1:
                return x2
            # 0 / x
            if isinstance(x2, Int) and x2.value == 0:
                return Int(0)
            return Div(x2, y2)

        case Let(name, value, body):
            return Let(name, _fold_expr(value), _fold_expr(body))

        case If(c, t, e):
            c2, t2, e2 = _fold_expr(c), _fold_expr(t), _fold_expr(e)
            if isinstance(c2, Bool):
                return t2 if c2.value else e2
            return If(c2, t2, e2)

        case Tuple(items):
            return Tuple([_fold_expr(i) for i in items])

        case Get(tup, idx):
            return Get(_fold_expr(tup), _fold_expr(idx))

        case Set(tup, idx, val):
            return Set(_fold_expr(tup), _fold_expr(idx), _fold_expr(val))

        case Do(eff, val):
            return Do(_fold_expr(eff), _fold_expr(val))

        case Lambda(params, body):
            return Lambda(params, _fold_expr(body))

        case Apply(f, args):
            return Apply(_fold_expr(f), [_fold_expr(a) for a in args])

        case Int() | Var() | Bool() | Unit():
            return expr

        case _:
            return expr
