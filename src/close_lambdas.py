from collections.abc import Callable
from functools import partial
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
    stmt = partial(close_statement, fresh=fresh)
    match statement:
        case Let(name, value, next):
            match value:
                case Lambda(parameters, body):
                    fvs = list(free_variables_expression(value))
                    env = fresh("env")

                    body: Statement = stmt(body)
                    for i, v in enumerate(fvs):
                        body = Let(v, Get(Var(env), Int(i + 1)), body)

                    code = fresh("code")
                    return Let(
                        code,
                        Lambda([env, *parameters], body),
                        Let(
                            name,
                            Tuple([Var(code), *[Var(v) for v in fvs]]),
                            stmt(next),
                        ),
                    )

                case value:
                    return Let(name, value, stmt(next))

        case If(condition, then, otherwise):
            return If(condition, stmt(then), stmt(otherwise))

        case Apply(callee, arguments):
            code = fresh("code")
            return Let(
                code,
                Get(callee, Int(0)),
                Apply(Var(code), [callee, *arguments]),
            )

        case Halt():
            return statement


def free_variables_statement(
    statement: Statement,
) -> set[str]:
    atom = partial(free_variables_atom)
    recur = partial(free_variables_statement)
    expr = partial(free_variables_expression)

    match statement:
        case Let(name, value, body):
            return expr(value) | (recur(body) - {name})

        case If(condition, then, otherwise):
            return atom(condition) | recur(then) | recur(otherwise)

        case Apply(callee, arguments):
            return atom(callee) | {fv for argument in arguments for fv in atom(argument)}

        case Halt(value):  # pragma: no branch
            return atom(value)


def free_variables_expression(
    expression: Expression,
) -> set[str]:
    atom = partial(free_variables_atom)
    stmt = partial(free_variables_statement)
    match expression:
        case Add(x, y) | Subtract(x, y) | Multiply(x, y) | LessThan(x, y) | EqualTo(x, y) | GreaterThanOrEqualTo(x, y):
            return atom(x) | atom(y)

        case Tuple(components):
            return {fv for component in components for fv in atom(component)}

        case Get(tuple, index):
            return atom(tuple) | atom(index)

        case Set(tuple, index, value):
            return atom(tuple) | atom(index) | atom(value)

        case Lambda(parameters, body):
            return stmt(body) - set(parameters)

        case Copy(value):  # pragma: no branch
            return atom(value)


def free_variables_atom(
    atom: Atom,
) -> set[str]:
    match atom:
        case Int():
            return set()
        case Var(x):
            return {x}
        case Bool():
            return set()
        case Unit():  # pragma: no branch
            return set()
