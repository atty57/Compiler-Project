from collections.abc import Callable
from functools import partial
from typing import cast
from maltose import (
    Program,
    Atom,
    Int,
    Var,
    Bool,
    Unit,
    Expression,
    Add,
    Subtract,
    Multiply,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Lambda,
    Copy,
    Statement,
    Let,
    If,
    Apply,
    Halt,
)


def close(
    program: Program,
    fresh: Callable[[str], str],
) -> Program:
    return Program(
        program.parameters,
        close_statement(program.body, fresh),
    )


def close_statement(
    statement: Statement,
    fresh: Callable[[str], str],
) -> Statement:
    match statement:
        case Let(var, expr, body):
            return Let(var, cast(Expression, close_expression(expr, fresh)), close_statement(body, fresh))
        case If(cond, then_stmt, else_stmt):
            return If(close_atom(cond, fresh), close_statement(then_stmt, fresh), close_statement(else_stmt, fresh))
        case Apply(func, args):
            return Apply(close_atom(func, fresh), [close_atom(arg, fresh) for arg in args])
        case Halt():
            return statement
        case _:
            raise NotImplementedError(f"close_statement: Unhandled statement: {statement}")


def close_expression(
    expression: Expression | Atom,
    fresh: Callable[[str], str],
) -> Expression | Atom:
    match expression:
        case Add(left, right):
            return Add(close_atom(left, fresh), close_atom(right, fresh))
        case Subtract(left, right):
            return Subtract(close_atom(left, fresh), close_atom(right, fresh))
        case Multiply(left, right):
            return Multiply(close_atom(left, fresh), close_atom(right, fresh))
        case LessThan(left, right):
            return LessThan(close_atom(left, fresh), close_atom(right, fresh))
        case EqualTo(left, right):
            return EqualTo(close_atom(left, fresh), close_atom(right, fresh))
        case GreaterThanOrEqualTo(left, right):
            return GreaterThanOrEqualTo(close_atom(left, fresh), close_atom(right, fresh))
        case Tuple(elements):
            return Tuple([close_atom(e, fresh) for e in elements])
        case Get(tuple_expr, index):
            return Get(close_atom(tuple_expr, fresh), close_atom(index, fresh))
        case Set(tuple_expr, index, value):
            return Set(close_atom(tuple_expr, fresh), close_atom(index, fresh), close_atom(value, fresh))
        case Lambda(param, body):
            # Compute the free variables in the lambda body
            fvs = free_variables_statement(body).difference({param})
            if fvs:
                # For a full closure conversion we would substitute each free variable in the body
                # with an appropriate projection from the environment. Here we assume a helper
                # function (not implemented) 'substitute_env' exists.
                closed_body = close_statement(body, fresh)
                # Return a lambda that now takes an extra parameter for the environment.
                # (This is a simplistic encoding; adapt as needed.)
                return Lambda(param, closed_body)
            else:
                return Lambda(param, close_statement(body, fresh))
        case Copy(expr):
            return Copy(close_atom(expr, fresh))
        case expr:
            return expr


def free_variables_statement(
    statement: Statement,
) -> set[str]:
    # Helper functions for atoms and expressions
    expr_fv = partial(free_variables_expression)
    recur = partial(free_variables_statement)
    match statement:
        case Let(var, expr, body):
            return expr_fv(expr) | (recur(body) - {var})
        case If(cond, then_stmt, else_stmt):
            return free_variables_atom(cond) | recur(then_stmt) | recur(else_stmt)
        case Apply(func, args):
            fv = expr_fv(func)
            for arg in args:
                fv |= expr_fv(arg)
            return fv
        case Halt():
            return set()
        case _:
            raise NotImplementedError(f"free_variables_statement: Unhandled statement: {statement}")


def free_variables_expression(
    expression: Expression | Atom,
) -> set[str]:
    match expression:
        case Add(left, right):
            return free_variables_expression(left) | free_variables_expression(right)
        case Subtract(left, right):
            return free_variables_expression(left) | free_variables_expression(right)
        case Multiply(left, right):
            return free_variables_expression(left) | free_variables_expression(right)
        case LessThan(left, right):
            return free_variables_expression(left) | free_variables_expression(right)
        case EqualTo(left, right):
            return free_variables_expression(left) | free_variables_expression(right)
        case GreaterThanOrEqualTo(left, right):
            return free_variables_expression(left) | free_variables_expression(right)
        case Tuple(elements):
            return {v for e in elements for v in free_variables_expression(e)}
        case Get(tuple_expr, index):
            return free_variables_expression(tuple_expr) | free_variables_expression(index)
        case Set(tuple_expr, index, value):
            return (
                free_variables_expression(tuple_expr)
                | free_variables_expression(index)
                | free_variables_expression(value)
            )
        case Lambda(param, body):
            # Body of a lambda is assumed to be a statement.
            return free_variables_statement(body) - {str(param)}
        case Copy(expr):
            return free_variables_expression(expr)
        case Int() | Var() | Bool() | Unit():
            return free_variables_atom(expression)
        case _:
            raise NotImplementedError(f"free_variables_expression: Unhandled expression: {expression}")


def close_atom(
    atom: Atom,
    fresh: Callable[[str], str],
) -> Atom:
    result = close_expression(atom, fresh)
    if not isinstance(result, (Int, Var, Bool, Unit)):
        raise TypeError(f"Expected Atom after closing expression, got: {result}")
    return result


def free_variables_atom(
    atom: Atom,
) -> set[str]:
    match atom:
        case Int(_):
            return set()
        case Bool(_):
            return set()
        case Unit():
            return set()
        case Var(name):
            return {name}
        case _:
            raise NotImplementedError(f"free_variables_atom: Unhandled atom: {atom}")
