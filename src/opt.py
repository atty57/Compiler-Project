from functools import partial
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var
from typing import Tuple, List

import kernel


# ---- Added helper functions for Add ----
def flatten_add(expr: Expression) -> Tuple[int, List[Expression]]:
    if isinstance(expr, Add):
        const_left, terms_left = flatten_add(expr.x)
        const_right, terms_right = flatten_add(expr.y)
        return (const_left + const_right, terms_left + terms_right)
    elif isinstance(expr, Int):
        return (expr.value, [])
    else:
        return (0, [expr])


def rebuild_add(const: int, terms: list[Expression]) -> Expression:
    if not terms:
        return Int(const)
    if const == 0:
        result = terms[0]
        for term in terms[1:]:
            result = Add(result, term)
        return result
    else:
        if len(terms) == 1:
            return Add(Int(const), terms[0])
        else:
            folded = terms[0]
            for term in terms[1:]:
                folded = Add(folded, term)
            return Add(Int(const), folded)


def opt(
    program: Program,
) -> Program:
    return Program(
        parameters=program.parameters,
        body=opt_expr(program.body),
    )


def opt_expr(
    expr: Expression,
) -> Expression:
    recur = partial(opt_expr)

    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            left = recur(e1)
            right = recur(e2)
            new_expr = Add(left, right)
            const, terms = flatten_add(new_expr)
            return rebuild_add(const, terms)

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case [e1, e2]:
                    return Subtract(e1, e2)

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [kernel.Int(i1), kernel.Int(i2)]:
                    return kernel.Int(i1 * i2)
                case [e1, e2]:
                    return Multiply(e1, e2)

        case Let(name, e1, e2):
            return Let(name, recur(e1), recur(e2))

        case Var(_):
            return expr
