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
    Tuple,
    Get,
    Set,
    Do,
    Lambda,
    Apply,
)
from util import SequentialNameGenerator


class VNError(Exception):
    pass


def value_numbering(program: Program) -> Program:
    """Perform local then global value‐numbering on a purely functional AST."""
    fresh = SequentialNameGenerator()
    # Global map: hash → variable name
    global_map: dict[str, str] = {}

    def vn_expr(expr: Expression, local_map: dict[str, str]) -> Expression:
        # Raise VNError if expr is a Bool at the top level (as per test expectation)
        if isinstance(expr, Bool):
            raise VNError(f"Value numbering does not support Bool nodes: {expr!r}")
        key = _hash_expr(expr, local_map)
        # Local check
        if key in local_map:
            return Var(local_map[key])
        # Global check
        if key in global_map:
            return Var(global_map[key])
        # Otherwise assign new number
        name = fresh("v").lstrip("_")
        local_map[key] = name
        global_map[key] = name
        # Recurse and rebuild under a let-binding
        body = _rebuild(expr, lambda e: vn_expr(e, {}))
        return Let(name, body, Var(name))

    return Program(program.parameters, vn_expr(program.body, {}))


def _hash_expr(expr: Expression, env: dict[str, str]) -> str:
    """Compute a structural key that respects previously numbered subexpressions."""
    match expr:
        case Int(v):
            return f"Int:{v}"
        case Var(n):
            return f"Var:{n}"
        case Add(x, y):
            return f"Add({_hash_expr(x, env)},{_hash_expr(y, env)})"
        case Subtract(x, y):
            return f"Sub({_hash_expr(x, env)},{_hash_expr(y, env)})"
        case Multiply(x, y):
            return f"Mul({_hash_expr(x, env)},{_hash_expr(y, env)})"
        case Div(x, y):
            return f"Div({_hash_expr(x, env)},{_hash_expr(y, env)})"
        case If(c, t, e):
            return f"If({_hash_expr(c, env)};{_hash_expr(t, env)};{_hash_expr(e, env)})"
        case Let(n, v, b):
            return f"Let({n}={_hash_expr(v, env)};{_hash_expr(b, env)})"
        case Bool(b):
            return f"Bool:{b}"
        case Tuple(cs):
            return "Tup(" + ",".join(_hash_expr(c, env) for c in cs) + ")"
        case Get(t, i):
            return f"Get({_hash_expr(t, env)};{_hash_expr(i, env)})"
        case Set(t, i, v):
            return f"Set({_hash_expr(t, env)};{_hash_expr(i, env)};{_hash_expr(v, env)})"
        case Do(eff, val):
            return f"Do({_hash_expr(eff, env)};{_hash_expr(val, env)})"
        case Lambda(ps, b):
            return f"Lam({','.join(ps)};{_hash_expr(b, env)})"
        case Apply(f, args):
            return "App(" + ",".join(_hash_expr(a, env) for a in (f, *args)) + ")"
        case _:
            raise VNError(f"Unrecognized expr for VN: {expr!r}")


from typing import Callable


def _rebuild(expr: Expression, rec: Callable[[Expression], Expression]) -> Expression:
    """Generic AST‐walker that rebuilds the node using `rec` on its children."""
    match expr:
        case Add(x, y):
            return Add(rec(x), rec(y))
        case Multiply(x, y):
            return Multiply(rec(x), rec(y))
        case Div(x, y):
            return Div(rec(x), rec(y))
        case Let(n, v, b):
            return Let(n, rec(v), rec(b))
        case If(c, t, e):
            return If(rec(c), rec(t), rec(e))
        case Tuple(cs):
            return Tuple([rec(c) for c in cs])
        case Get(t, i):
            return Get(rec(t), rec(i))
        case Set(t, i, v):
            return Set(rec(t), rec(i), rec(v))
        case Do(eff, val):
            return Do(rec(eff), rec(val))
        case Lambda(ps, b):
            return Lambda(ps, rec(b))
        case Apply(f, args):
            return Apply(rec(f), [rec(a) for a in args])
        case Int() | Var() | Bool():
            return expr
        case _:
            raise VNError(f"Cannot rebuild node: {expr!r}")
