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
        case kernel.Int(i):
            return kernel.Int(i)
        case kernel.Add(x, y):
            return kernel.Add(recur(x), recur(y))
        case kernel.Subtract(x, y):
            return kernel.Subtract(recur(x), recur(y))
        case kernel.Multiply(x, y):
            return kernel.Multiply(recur(x), recur(y))
        case kernel.Let(x, e1, e2):
            return kernel.Let(x, recur(e1), recur(e2))
        case kernel.Var(x):
            return kernel.Var(x)
        case kernel.Bool(b):
            return kernel.Bool(b)
        case kernel.If(c, t, f):
            return kernel.If(recur(c), recur(t), recur(f))
            
        # Additional sugar constructs (unchanged)
        case sugar.Sum(operands):
            if not operands:
                return kernel.Int(0)
            elif len(operands) == 1:
                return recur(operands[0])
            else:
                return kernel.Add(recur(operands[0]), recur(sugar.Sum(operands[1:])))
        case sugar.Difference(operands):
            if len(operands) == 1:
                return kernel.Subtract(kernel.Int(0), recur(operands[0]))
            elif len(operands) == 2:
                return kernel.Subtract(recur(operands[0]), recur(operands[1]))
            else:
                return kernel.Subtract(recur(operands[0]), recur(sugar.Difference(operands[1:])))
        case sugar.Product(operands):
            if not operands:
                return kernel.Int(1)
            elif len(operands) == 1:
                return recur(operands[0])
            else:
                return kernel.Multiply(recur(operands[0]), recur(sugar.Product(operands[1:])))
        case sugar.LetStar(bindings, body):
            if not bindings:
                return recur(body)
            else:
                (x, e) = bindings[0]
                rest = bindings[1:]
                # Desugar LetStar into nested Let: let x = e in (let* rest in body)
                return kernel.Let(x, recur(e), recur(sugar.LetStar(rest, body)))
        case sugar.Cond(arms, default):
            if not arms:
                return recur(default)
            else:
                (c, a), *rest = arms
                return kernel.If(recur(c), recur(a), recur(sugar.Cond(rest, default)))
        case sugar.Not(x):
            return kernel.If(recur(x), kernel.Bool(False), kernel.Bool(True))
        case sugar.All(operands):
            if not operands:
                return kernel.Bool(True)
            elif len(operands) == 1:
                return recur(operands[0])
            else:
                return kernel.If(recur(operands[0]), recur(sugar.All(operands[1:])), kernel.Bool(False))
        case sugar.Any(operands):
            if not operands:
                return kernel.Bool(False)
            elif len(operands) == 1:
                return recur(operands[0])
            else:
                return kernel.If(recur(operands[0]), kernel.Bool(True), recur(sugar.Any(operands[1:])))
        case sugar.NonDescending(operands):
            if len(operands) <= 1:
                return kernel.Bool(True)
            else:
                a = recur(operands[0])
                b = recur(operands[1])
                rest = sugar.NonDescending(operands[1:])
                # a <= b is true if either a < b or a == b.
                cond = kernel.If(kernel.LessThan(a, b), kernel.Bool(True), kernel.EqualTo(a, b))
                return kernel.If(cond, recur(rest), kernel.Bool(False))
        case sugar.Ascending(operands):
            if len(operands) <= 1:
                return kernel.Bool(True)
            else:
                a = recur(operands[0])
                b = recur(operands[1])
                rest = sugar.Ascending(operands[1:])
                return kernel.If(kernel.LessThan(a, b), recur(rest), kernel.Bool(False))
        case sugar.Same(operands):
            if len(operands) <= 1:
                return kernel.Bool(True)
            else:
                a = recur(operands[0])
                b = recur(operands[1])
                rest = sugar.Same(operands[1:])
                return kernel.If(kernel.EqualTo(a, b), recur(rest), kernel.Bool(False))
        case sugar.Descending(operands):
            if len(operands) <= 1:
                return kernel.Bool(True)
            else:
                a = recur(operands[0])
                b = recur(operands[1])
                rest = sugar.Descending(operands[1:])
                return kernel.If(kernel.LessThan(b, a), recur(rest), kernel.Bool(False))
        case sugar.NonAscending(operands):
            if len(operands) <= 1:
                return kernel.Bool(True)
            else:
                a = recur(operands[0])
                b = recur(operands[1])
                rest = sugar.NonAscending(operands[1:])
                return kernel.If(kernel.LessThan(a, b), kernel.Bool(False), recur(rest))
        case _:
            raise NotImplementedError(f"Desugaring not implemented for: {expr}")
