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
                    return kernel.Binary("+", recur(first), recur(sugar.Add(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Subtract(es):
            match es:
                case [first]:
                    return kernel.Binary("-", kernel.Int(0), recur(first))
                case [first, second]:
                    return kernel.Binary("-", recur(first), recur(second))
                case [first, *rest]:
                    return kernel.Binary("-", recur(first), recur(sugar.Subtract(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Multiply(es):
            match es:
                case []:
                    return kernel.Int(1)
                case [first, *rest]:
                    return kernel.Binary("*", recur(first), recur(sugar.Multiply(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Let(x, e1, e2):
            return kernel.Let(x, recur(e1), recur(e2))

        case sugar.Var(x):  # pragma: no branch
            return kernel.Var(x)

        case sugar.Bool(b):
            return kernel.Bool(b)

        case sugar.Not(e1):
            return kernel.If(
                kernel.Binary("==", recur(e1), kernel.Bool(True)),
                kernel.Bool(False),
                kernel.Bool(True),
            )

        case sugar.And(es):
            match es:
                case []:
                    return kernel.Bool(True)
                case [first, *rest]:
                    return kernel.If(recur(first), recur(sugar.And(rest)), kernel.Bool(True))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Or(es):
            match es:
                case []:
                    return kernel.Bool(False)
                case [first, *rest]:
                    return kernel.If(recur(first), kernel.Bool(True), recur(sugar.Or(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.If(e1, e2, e3):
            return kernel.If(recur(e1), recur(e2), recur(e3))

        case sugar.LessThan(es):
            match es:
                case [first, second]:
                    return kernel.Binary("<", recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(sugar.And([sugar.LessThan([first, second]), sugar.LessThan([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.LessThanOrEqualTo(es):
            match es:
                case [first, second]:
                    return kernel.Binary(">=", recur(second), recur(first))
                case [first, second, *rest]:
                    return recur(
                        sugar.And([sugar.LessThanOrEqualTo([first, second]), sugar.LessThanOrEqualTo([second, *rest])])
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.EqualTo(es):
            match es:
                case [first, second]:
                    return kernel.Binary("==", recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(sugar.And([sugar.EqualTo([first, second]), sugar.EqualTo([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThan(es):
            match es:
                case [first, second]:
                    return kernel.Binary("<", recur(second), recur(first))
                case [first, second, *rest]:
                    return recur(sugar.And([sugar.GreaterThan([first, second]), sugar.GreaterThan([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThanOrEqualTo(es):  # pragma: no branch
            match es:
                case [first, second]:
                    return kernel.Binary(">=", recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(
                        sugar.And(
                            [sugar.GreaterThanOrEqualTo([first, second]), sugar.GreaterThanOrEqualTo([second, *rest])]
                        )
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()
