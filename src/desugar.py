from functools import partial
import sugar
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
        case sugar.Int(i):
            return kernel.Int(i)

        case sugar.Add(es):
            match es:
                case []:
                    return kernel.Int(0)
                case [first, *rest]:
                    return kernel.Add(recur(first), recur(sugar.Add(rest)))
                case _:
                    pass

        case sugar.Subtract(es):
            match es:
                case []:
                    return kernel.Int(0)
                case [first, *rest]:
                    if not rest:
                        return kernel.Subtract(kernel.Int(0), recur(first))
                    else:
                        return kernel.Subtract(recur(first), recur(sugar.Subtract(rest)))
                case _:
                    pass

        case sugar.Multiply(es):
            match es:
                case []:
                    return kernel.Int(1)
                case [first, *rest]:
                    return kernel.Multiply(recur(first), recur(sugar.Multiply(rest)))
                case _:
                    pass

        case sugar.Let(x, e1, e2):
            return kernel.Let(x, recur(e1), recur(e2))

        case sugar.Var(x):  # pragma: no branch
            return kernel.Var(x)
