from collections.abc import Callable, Mapping
from functools import partial
import kernel
import monadic


def remove_complex_operands(
    program: kernel.Program,
    fresh: Callable[[str], str],
) -> monadic.Program:
    return monadic.Program(
        program.parameters,
        rco_expr(program.body, fresh),
    )


type Binding = tuple[str, monadic.Expression]


def rco_expr(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
) -> monadic.Expression:
    to_expr = partial(rco_expr, fresh=fresh)
    to_atom = partial(rco_atom, fresh=fresh)

    match expr:
        case kernel.Int(i):
            return monadic.Int(i)

        case kernel.Add(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            return wrap({**b1, **b2}, monadic.Add(a1, a2))

        case kernel.Let(x, e1, e2):
            return monadic.Let(x, to_expr(e1), to_expr(e2))

        case kernel.Var(x):
            return monadic.Var(x)

        case kernel.If(e1, e2, e3):
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            e3 = to_expr(e3)
            return monadic.If(e1, e2, e3)


def rco_atom(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
) -> tuple[str, Mapping[str, monadic.Expression]]:
    to_expr = partial(rco_expr, fresh=fresh)
    to_atom = partial(rco_atom, fresh=fresh)

    match expr:
        case kernel.Int(i):
            tmp = fresh("t")
            return tmp, {tmp: monadic.Int(i)}

        case kernel.Add(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return tmp, {**b1, **b2, tmp: monadic.Add(a1, a2)}

        case kernel.Subtract(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return tmp, {**b1, **b2, tmp: monadic.Subtract(a1, a2)}

        case kernel.Multiply(e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return tmp, {**b1, **b2, tmp: monadic.Multiply(a1, a2)}

        case kernel.Var(x):
            return x, {}

        case kernel.Let(x, e1, e2):
            a2, b2 = to_atom(e2)
            return a2, {x: to_expr(e1), **b2}

        case kernel.If(e1, e2, e3):
            e1 = to_expr(e1)
            e2 = to_expr(e2)
            e3 = to_expr(e3)
            tmp = fresh("t")
            return tmp, {tmp: monadic.If(e1, e2, e3)}

        case kernel.Compare(operator, e1, e2):
            a1, b1 = to_atom(e1)
            a2, b2 = to_atom(e2)
            tmp = fresh("t")
            return tmp, {**b1, **b2, tmp: monadic.Add(a1, a2)}


def wrap(
    bindings: Mapping[str, monadic.Expression],
    expr: monadic.Expression,
) -> monadic.Expression:
    for x, e in reversed(list(bindings.items())):
        expr = monadic.Let(x, e, expr)
    return expr
