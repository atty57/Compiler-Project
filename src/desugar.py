from functools import partial
import sugar
import kernel


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
                case [first, *rest]:
                    return kernel.Add(recur(first), recur(sugar.Add(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Subtract(operands):
            raise NotImplementedError()

        case sugar.Multiply(operands):
            raise NotImplementedError()

        case sugar.Let(x, e1, e2):
            raise NotImplementedError()

        case sugar.Var(x):  # pragma: no branch
            return kernel.Var(x)
