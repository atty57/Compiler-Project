from functools import partial
import sugar
import kernel

from sugar import (
    Sum,
    Difference,
    Product,
    LetStar,
    Cond,
    Not,
    All,
    Any,
    NonAscending,
    Descending,
    Same,
    Ascending,
    NonDescending,
)
from kernel import (
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
)


def desugar(
    program: sugar.Program,
) -> kernel.Program:
    return kernel.Program(
        parameters=program.parameters,
        body=desugar_expr(program.body),
    )


def desugar_expr(
    expr: sugar.Expression,
) -> kernel.Expression:
    recur = partial(desugar_expr)
    match expr:
        # Basic constructs – note we now match on kernel.* instead of sugar.*
        case Int(i):
            return Int(i)
        case Add(x, y):
            return Add(recur(x), recur(y))
        case Subtract(x, y):
            return Subtract(recur(x), recur(y))
        case Multiply(x, y):
            return Multiply(recur(x), recur(y))
        case Let(x, e1, e2):
            return Let(x, recur(e1), recur(e2))
        case Var(x):
            return Var(x)
        case Bool(b):
            return Bool(b)
        case If(c, t, f):
            return If(recur(c), recur(t), recur(f))
        case LessThan(x, y):
            return LessThan(recur(x), recur(y))
        case EqualTo(x, y):
            return EqualTo(recur(x), recur(y))
        case GreaterThanOrEqualTo(x, y):
            return GreaterThanOrEqualTo(recur(x), recur(y))

        # Additional sugar constructs (unchanged)
        case Sum(operands):
            if not operands:
                return Int(0)
            elif len(operands) == 1:
                return Add(recur(operands[0]), Int(0))
            else:
                return Add(recur(operands[0]), recur(Sum(operands[1:])))

        case Difference(operands):
            if len(operands) == 1:
                return Subtract(Int(0), recur(operands[0]))
            elif len(operands) == 2:
                return Subtract(recur(operands[0]), recur(operands[1]))
            else:
                return Subtract(recur(operands[0]), recur(Difference(operands[1:])))

        case Product(operands):
            if not operands:
                return Int(1)
            elif len(operands) == 1:
                return Multiply(recur(operands[0]), Int(1))
            else:
                return Multiply(recur(operands[0]), recur(Product(operands[1:])))

        case LetStar(bindings, body):
            if not bindings:
                return recur(body)
            else:
                (x, e) = bindings[0]
                rest = bindings[1:]
                # Desugar LetStar into nested Let: let x = e in (let* rest in body)
                return Let(x, recur(e), recur(LetStar(rest, body)))

        case Cond(arms, default):
            if not arms:
                return recur(default)
            else:
                (c, a), *rest = arms
                return If(recur(c), recur(a), recur(Cond(rest, default)))

        # Modified Not case: use EqualTo to check for Bool(True)
        case Not(x):
            return If(EqualTo(recur(x), Bool(True)), Bool(False), Bool(True))

        case All(operands):
            if not operands:
                return Bool(True)
            elif len(operands) == 1:
                return If(recur(operands[0]), Bool(True), Bool(False))
            else:
                return If(recur(operands[0]), recur(All(operands[1:])), Bool(False))

        # Modified Any case: always produce an If–expression even for one operand
        case Any(operands):
            if not operands:
                return Bool(False)
            elif len(operands) == 1:
                return If(recur(operands[0]), Bool(True), Bool(False))
            else:
                return If(recur(operands[0]), Bool(True), recur(Any(operands[1:])))

        case NonDescending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return Bool(True)
            elif len(operands) == 2:
                return GreaterThanOrEqualTo(recur(operands[1]), recur(operands[0]))
            else:
                return If(
                    GreaterThanOrEqualTo(recur(operands[1]), recur(operands[0])),
                    recur(NonDescending(operands[1:])),
                    Bool(False),
                )

        case Ascending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return Bool(True)
            elif len(operands) == 2:
                return LessThan(recur(operands[0]), recur(operands[1]))
            else:
                return If(
                    LessThan(recur(operands[0]), recur(operands[1])),
                    recur(Ascending(operands[1:])),
                    Bool(False),
                )

        case Same(operands):
            if len(operands) == 0 or len(operands) == 1:
                return Bool(True)
            elif len(operands) == 2:
                return EqualTo(recur(operands[0]), recur(operands[1]))
            else:
                return If(
                    EqualTo(recur(operands[0]), recur(operands[1])),
                    recur(Same(operands[1:])),
                    Bool(False),
                )

        case Descending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return Bool(True)
            elif len(operands) == 2:
                return LessThan(recur(operands[1]), recur(operands[0]))
            else:
                return If(
                    LessThan(recur(operands[1]), recur(operands[0])),
                    recur(Descending(operands[1:])),
                    Bool(False),
                )

        case NonAscending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return Bool(True)
            elif len(operands) == 2:
                return GreaterThanOrEqualTo(recur(operands[0]), recur(operands[1]))
            else:
                return If(
                    GreaterThanOrEqualTo(recur(operands[0]), recur(operands[1])),
                    recur(NonAscending(operands[1:])),
                    Bool(False),
                )

        case _:
            raise NotImplementedError(f"Desugaring not implemented for: {expr}")
