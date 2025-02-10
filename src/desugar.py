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
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Subtract(es):
            raise NotImplementedError()

        case sugar.Multiply(es):
            raise NotImplementedError()

        case sugar.Let(x, e1, e2):
            raise NotImplementedError()

        case sugar.Var(x):  # pragma: no branch
            return kernel.Var(x)
