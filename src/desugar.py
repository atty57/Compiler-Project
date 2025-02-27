from functools import partial
import sugar
import kernel

from sugar import (
    Int,
    Let,
    Var,
    LetStar,
    Bool,
    Not,
    All,
    Any,
    If,
    Cond,
    Unit,
    Cell,
    Get,
    Set,
    While,
)
import kernel


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
        case Int():
            return expr

        case sugar.Add(es):
            match es:
                case []:
                    return Int(0)
                case [first, *rest]:
                    return kernel.Add(recur(first), recur(sugar.Add(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Subtract(es):
            match es:
                case [first]:
                    return kernel.Subtract(Int(0), recur(first))
                case [first, second]:
                    return kernel.Subtract(recur(first), recur(second))
                case [first, *rest]:
                    return kernel.Subtract(recur(first), recur(sugar.Subtract(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Multiply(es):
            match es:
                case []:
                    return Int(1)
                case [first, *rest]:
                    return kernel.Multiply(recur(first), recur(sugar.Multiply(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Let(x, e1, e2):
            return Let(x, recur(e1), recur(e2))
        case Var(x):
            return Var(x)
        case Bool(b):
            return Bool(b)
        case If(c, t, f):
            return If(recur(c), recur(t), recur(f))
        case sugar.LessThan(x, y):
            return kernel.LessThan(recur(x), recur(y))
        case sugar.EqualTo(x, y):
            return kernel.EqualTo(recur(x), recur(y))
        case sugar.GreaterThanOrEqualTo(x, y):
            return kernel.GreaterThanOrEqualTo(recur(x), recur(y))

        # Additional sugar constructs (unchanged)
        case sugar.Sum(operands):
            if not operands:
                return kernel.Int(0)
            elif len(operands) == 1:
                return kernel.Add(recur(operands[0]), kernel.Int(0))
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
                return kernel.Multiply(recur(operands[0]), kernel.Int(1))
            else:
                return kernel.Multiply(recur(operands[0]), recur(sugar.Product(operands[1:])))

        case sugar.LetStar(bindings, body):
            if not bindings:
                recur(body)
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

        # Modified Not case: use EqualTo to check for Bool(True)
        case sugar.Not(x):
            return kernel.If(kernel.EqualTo(recur(x), kernel.Bool(True)), kernel.Bool(False), kernel.Bool(True))

        case sugar.All(operands):
            if not operands:
                return kernel.Bool(True)
            elif len(operands) == 1:
                return kernel.If(recur(operands[0]), kernel.Bool(True), kernel.Bool(False))
            else:
                return kernel.If(recur(operands[0]), recur(sugar.All(operands[1:])), kernel.Bool(False))

        # Modified Any case: always produce an If–expression even for one operand
        case sugar.Any(operands):
            if not operands:
                return kernel.Bool(False)
            elif len(operands) == 1:
                return kernel.If(recur(operands[0]), kernel.Bool(True), kernel.Bool(False))
            else:
                return kernel.If(recur(operands[0]), kernel.Bool(True), recur(sugar.Any(operands[1:])))

        case sugar.NonDescending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return kernel.Bool(True)
            elif len(operands) == 2:
                return kernel.GreaterThanOrEqualTo(recur(operands[1]), recur(operands[0]))
            else:
                return kernel.If(
                    kernel.GreaterThanOrEqualTo(recur(operands[1]), recur(operands[0])),
                    recur(sugar.NonDescending(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.Ascending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return kernel.Bool(True)
            elif len(operands) == 2:
                return kernel.LessThan(recur(operands[0]), recur(operands[1]))
            else:
                return kernel.If(
                    kernel.LessThan(recur(operands[0]), recur(operands[1])),
                    recur(sugar.Ascending(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.Same(operands):
            if len(operands) == 0 or len(operands) == 1:
                return kernel.Bool(True)
            elif len(operands) == 2:
                return kernel.EqualTo(recur(operands[0]), recur(operands[1]))
            else:
                return kernel.If(
                    kernel.EqualTo(recur(operands[0]), recur(operands[1])),
                    recur(sugar.Same(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.Descending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return kernel.Bool(True)
            elif len(operands) == 2:
                return kernel.LessThan(recur(operands[1]), recur(operands[0]))
            else:
                return kernel.If(
                    kernel.LessThan(recur(operands[1]), recur(operands[0])),
                    recur(sugar.Descending(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.NonAscending(operands):
            if len(operands) == 0 or len(operands) == 1:
                return kernel.Bool(True)
            elif len(operands) == 2:
                return kernel.GreaterThanOrEqualTo(recur(operands[0]), recur(operands[1]))
            else:
                return kernel.If(
                    kernel.GreaterThanOrEqualTo(recur(operands[0]), recur(operands[1])),
                    recur(sugar.NonAscending(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.LessThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.GreaterThanOrEqualTo(recur(second), recur(first))
                case [first, second, *rest]:
                    return If(
                        kernel.GreaterThanOrEqualTo(recur(second), recur(first)),
                        recur(sugar.LessThanOrEqualTo([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.LessThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.LessThan(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        kernel.LessThan(recur(first), recur(second)),
                        recur(sugar.LessThan([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.EqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.EqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        kernel.EqualTo(recur(first), recur(second)),
                        recur(sugar.EqualTo([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.LessThan(recur(second), recur(first))
                case [first, second, *rest]:
                    return If(
                        kernel.LessThan(recur(second), recur(first)),
                        recur(sugar.GreaterThan([second, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThanOrEqualTo(es):  # pragma: no branch
            match es:
                case [] | [_]:
                    return Bool(True)
                case [first, second]:
                    return kernel.GreaterThanOrEqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return If(
                        kernel.GreaterThanOrEqualTo(recur(first), recur(second)),
                        recur(sugar.GreaterThanOrEqualTo([second, *rest])),
                        Bool(False),
                    )

                case _:  # pragma: no cover
                    raise NotImplementedError()

        case _:  # pragma: no branch
            raise NotImplementedError()
