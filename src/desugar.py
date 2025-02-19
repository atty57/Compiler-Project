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
        case sugar.Int(i):
            return kernel.Int(i)

        case sugar.Add(es):
            match es:
                case []:
                    return kernel.Int(0)
                case [first, *rest]:  # pragma: no branch
                    return kernel.Add(recur(first), recur(sugar.Add(rest)))

        case sugar.Subtract(es):
            match es:
                case [first]:  # Single operand: Convert to (0 - first)
                    return kernel.Subtract(kernel.Int(0), recur(first))
                case [first, second]:  # Two operands: Convert directly
                    return kernel.Subtract(recur(first), recur(second))
                case [first, *rest]:  # pragma: no branch # More than two operands: Nest subtraction
                    return kernel.Subtract(recur(first), recur(sugar.Subtract(rest)))

        case sugar.Multiply(es):
            match es:
                case []:
                    return kernel.Int(1)
                case [first, *rest]:  # pragma: no branch
                    return kernel.Multiply(recur(first), recur(sugar.Multiply(rest)))

        case sugar.Let(x, e1, e2):
            return kernel.Let(x, recur(e1), recur(e2))

        case sugar.Var(x):  # pragma: no branch
            return kernel.Var(x)
