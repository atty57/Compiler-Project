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
                    env = fresh("t")

                    body: Statement = stmt(body)
                    for i, v in enumerate(fvs):
                        body = Let(v, Get(Var(env), Int(i + 1)), body)

                    code = fresh("t")
                    return Let(
                        code,
                        Lambda([env, *parameters], body),
                        Let(
                            name,
                            Tuple([Var(code), *[Var(v) for v in fvs]]),
                            stmt(next),
                        ),
                    )

                case value:  # pragma: no branch
                    return Let(name, value, stmt(next))

        case If(condition, then, otherwise):
            return If(condition, stmt(then), stmt(otherwise))

        case Apply(callee, arguments):
            if not arguments:
                t = fresh("t")
                return Let(t, Get(callee, Int(0)), Apply(Var(t), [callee]))
            else:
                k = fresh("k")
                return Let(
                    k,
                    Lambda(["_t0"], Halt(Var("_t0"))),
                    Apply(close_atom(callee, fresh), [close_atom(arg, fresh) for arg in arguments] + [Var(k)]),
                )

        case Halt(value):  # pragma: no branch
            return Halt(close_atom(value, fresh))

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

        case Lambda(parameters, body):
            # Possibly your existing lambda-conversion code:
            fvs = free_variables_statement(body) - set(parameters)
            env_param = fresh("t")
            new_params = [env_param] + list(parameters)
            closed_body = close_statement(body, fresh)
            if fvs:
                for idx, fv in enumerate(sorted(fvs), start=1):
                    closed_body = Let(fv, Get(Var(env_param), Int(idx)), closed_body)
            return Lambda(new_params, closed_body)

        case Copy(expr):
            return Copy(close_atom(expr, fresh))
        case expr:
            return expr


def close_lambda_with_env(
    lambda_expr: Lambda[Statement],
    env_param: str,
    fresh: Callable[[str], str],
) -> Lambda[Statement]:
    parameters = lambda_expr.parameters
    body = lambda_expr.body
    fvs = free_variables_statement(body) - set(parameters)
    new_params = [env_param] + list(parameters)
    closed_body = close_statement(body, fresh)
    if fvs:
        for idx, fv in enumerate(sorted(fvs), start=1):
            closed_body = Let(fv, Get(Var(env_param), Int(idx)), closed_body)
    return Lambda(new_params, closed_body)


def free_variables_statement(
    statement: Statement,
) -> set[str]:
    atom_fv = free_variables_atom
    expr_fv = free_variables_expression
    recur = free_variables_statement

    match statement:
        case Let(name, value, body):
            return expr_fv(value) | (recur(body) - {name})

        case If(condition, then, otherwise):
            return atom_fv(condition) | recur(then) | recur(otherwise)

        case Apply(callee, arguments):
            return atom_fv(callee) | {fv for argument in arguments for fv in atom_fv(argument)}

        case Halt(value):  # pragma: no branch
            return atom_fv(value)


def free_variables_expression(
    expression: Expression | Atom,
) -> set[str]:
    atom_fv = free_variables_atom
    stmt_fv = free_variables_statement

    match expression:
        case Add(x, y) | Subtract(x, y) | Multiply(x, y) | LessThan(x, y) | EqualTo(x, y) | GreaterThanOrEqualTo(x, y):
            return atom_fv(x) | atom_fv(y)

        case Tuple(components):
            return {fv for component in components for fv in atom_fv(component)}

        case Get(tuple, index):
            return atom_fv(tuple) | atom_fv(index)

        case Set(tuple, index, value):
            return atom_fv(tuple) | atom_fv(index) | atom_fv(value)

        case Lambda(parameters, body):
            return stmt_fv(body) - set(parameters)

        case Copy(value):  # pragma: no branch
            return atom_fv(value)

        case Int() | Bool() | Unit():
            return set()

        case Var(name):
            return {name}

        case _:
            return set()


def close_atom(
    atom: Atom,
    fresh: Callable[[str], str],
) -> Atom:
    e = close_expression(atom, fresh)
    if not isinstance(e, (Int, Var, Bool, Unit)):
        raise TypeError(f"Expected Atom, got {e}")
    return e


def free_variables_atom(atom: Atom) -> set[str]:
    match atom:
        case Int():
            return set()
        case Var(x):
            return {x}
        case Bool():
            return set()
        case Unit():  # pragma: no branch
            return set()
        case _:
            return set()
