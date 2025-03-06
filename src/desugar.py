from functools import partial
import sugar
import kernel


def desugar(program: sugar.Program) -> kernel.Program:
    return kernel.Program(
        parameters=program.parameters,
        body=desugar_expr(program.body),
    )


def desugar_expr(expr: sugar.Expression) -> kernel.Expression:
    recur = partial(desugar_expr)

    # --- Added fixes for sugar.LessThan, EqualTo, GreaterThan,
    #     GreaterThanOrEqualTo, and LessThanOrEqualTo ---
    if isinstance(expr, sugar.LessThan):
        es = expr.operands
        if len(es) <= 1:
            return kernel.Bool(True)
        elif len(es) == 2:
            return kernel.LessThan(recur(es[0]), recur(es[1]))
        else:
            return kernel.If(
                kernel.LessThan(recur(es[0]), recur(es[1])),
                recur(sugar.LessThan(operands=es[1:])),
                kernel.Bool(False),
            )
    if isinstance(expr, sugar.EqualTo):
        es = expr.operands
        if len(es) <= 1:
            return kernel.Bool(True)
        elif len(es) == 2:
            return kernel.EqualTo(recur(es[0]), recur(es[1]))
        else:
            return kernel.If(
                kernel.EqualTo(recur(es[0]), recur(es[1])),
                recur(sugar.EqualTo(operands=es[1:])),
                kernel.Bool(False),
            )
    if isinstance(expr, sugar.GreaterThan):
        es = expr.operands
        if len(es) <= 1:
            return kernel.Bool(True)
        elif len(es) == 2:
            # x > y  ==>  y < x
            return kernel.LessThan(recur(es[1]), recur(es[0]))
        else:
            return kernel.If(
                kernel.LessThan(recur(es[1]), recur(es[0])),
                recur(sugar.GreaterThan(operands=es[1:])),
                kernel.Bool(False),
            )
    if isinstance(expr, sugar.GreaterThanOrEqualTo):
        es = expr.operands
        if len(es) <= 1:
            return kernel.Bool(True)
        elif len(es) == 2:
            return kernel.GreaterThanOrEqualTo(recur(es[0]), recur(es[1]))
        else:
            return kernel.If(
                kernel.GreaterThanOrEqualTo(recur(es[0]), recur(es[1])),
                recur(sugar.GreaterThanOrEqualTo(operands=es[1:])),
                kernel.Bool(False),
            )
    if isinstance(expr, sugar.LessThanOrEqualTo):
        es = expr.operands
        if len(es) <= 1:
            return kernel.Bool(True)
        elif len(es) == 2:
            # x <= y  ==>  y >= x
            return kernel.GreaterThanOrEqualTo(recur(es[1]), recur(es[0]))
        else:
            return kernel.If(
                kernel.GreaterThanOrEqualTo(recur(es[1]), recur(es[0])),
                recur(sugar.LessThanOrEqualTo(operands=es[1:])),
                kernel.Bool(False),
            )
    # -------------------------------------------------------------------

    match expr:
        case sugar.Int():
            # sugar.Int is effectively the same class as kernel.Int
            return expr

        case sugar.Add(es):
            match es:
                case []:
                    return kernel.Int(0)
                case [first, *rest]:
                    return kernel.Add(recur(first), recur(sugar.Add(rest)))
                case _:
                    raise NotImplementedError()

        case sugar.Subtract(es):
            match es:
                case [first]:
                    return kernel.Subtract(kernel.Int(0), recur(first))
                case [first, second]:
                    return kernel.Subtract(recur(first), recur(second))
                case [first, *rest]:
                    return kernel.Subtract(recur(first), recur(sugar.Subtract(rest)))
                case _:
                    raise NotImplementedError()

        case sugar.Multiply(es):
            match es:
                case []:
                    return kernel.Int(1)
                case [first, *rest]:
                    return kernel.Multiply(recur(first), recur(sugar.Multiply(rest)))
                case _:
                    raise NotImplementedError()

        case sugar.Let(x, e1, e2):
            return kernel.Let(x, recur(e1), recur(e2))

        case sugar.Var(x):
            return kernel.Var(x)

        case sugar.Bool(b):
            return kernel.Bool(b)

        case sugar.If(c, t, f):
            return kernel.If(recur(c), recur(t), recur(f))

        # ----------------------------------------------------------------------
        # Additional sugar constructs (multi-operand expansions).
        # ----------------------------------------------------------------------

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
                return recur(body)
            else:
                (x, e) = bindings[0]
                rest = bindings[1:]
                return kernel.Let(x, recur(e), recur(sugar.LetStar(rest, body)))

        case sugar.Cond(arms, default):
            if not arms:
                return recur(default)
            else:
                (c, a), *rest = arms
                return kernel.If(recur(c), recur(a), recur(sugar.Cond(rest, default)))

        case sugar.Not(x):
            # Desugar Not(...) => if x == True then False else True
            return kernel.If(
                kernel.EqualTo(recur(x), kernel.Bool(True)),
                kernel.Bool(False),
                kernel.Bool(True),
            )

        case sugar.All(operands):
            if not operands:
                return kernel.Bool(True)
            elif len(operands) == 1:
                return kernel.If(recur(operands[0]), kernel.Bool(True), kernel.Bool(False))
            else:
                return kernel.If(
                    recur(operands[0]),
                    recur(sugar.All(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.Any(operands):
            if not operands:
                return kernel.Bool(False)
            elif len(operands) == 1:
                return kernel.If(recur(operands[0]), kernel.Bool(True), kernel.Bool(False))
            else:
                return kernel.If(recur(operands[0]), kernel.Bool(True), recur(sugar.Any(operands[1:])))

        case sugar.NonDescending(operands):
            if len(operands) <= 1:
                return kernel.Bool(True)
            elif len(operands) == 2:
                # x <= y  =>  y >= x
                return kernel.GreaterThanOrEqualTo(recur(operands[1]), recur(operands[0]))
            else:
                return kernel.If(
                    kernel.GreaterThanOrEqualTo(recur(operands[1]), recur(operands[0])),
                    recur(sugar.NonDescending(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.Ascending(operands):
            if len(operands) <= 1:
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
            if len(operands) <= 1:
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
            if len(operands) <= 1:
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
            if len(operands) <= 1:
                return kernel.Bool(True)
            elif len(operands) == 2:
                # x >= y
                return kernel.GreaterThanOrEqualTo(recur(operands[0]), recur(operands[1]))
            else:
                return kernel.If(
                    kernel.GreaterThanOrEqualTo(recur(operands[0]), recur(operands[1])),
                    recur(sugar.NonAscending(operands[1:])),
                    kernel.Bool(False),
                )

        case sugar.Do(operands):
            if not operands:
                return kernel.Unit()
            elif len(operands) == 1:
                return recur(operands[0])
            else:
                first = operands[0]
                rest = operands[1:]
                if len(rest) == 1:
                    return kernel.Do(recur(first), recur(rest[0]))
                else:
                    return kernel.Do(recur(first), recur(sugar.Do(rest)))

        case sugar.While(condition, body):
            return kernel.While(recur(condition), recur(body))

        case sugar.Unit():
            return kernel.Unit()

        case sugar.Cell(val):
            return kernel.Cell(recur(val))

        case sugar.Get(cell):
            return kernel.Get(recur(cell))

        case sugar.Set(cell, value):
            return kernel.Set(recur(cell), recur(value))

        # If none of the above cases match:
        case _:
            raise ValueError(f"Unsupported expression type: {type(expr)}")
