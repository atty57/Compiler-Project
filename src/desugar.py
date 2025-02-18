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
        case kernel.Int():
            return expr

        case sugar.Add(es):
            match es:
                case []:
                    return kernel.Int(0)
                case [first, *rest]:
                    return kernel.Add(recur(first), recur(sugar.Add(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Subtract(es):
            match es:
                case [first]:
                    return kernel.Subtract(kernel.Int(0), recur(first))
                case [first, second]:
                    return kernel.Subtract(recur(first), recur(second))
                case [first, *rest]:
                    return kernel.Subtract(recur(first), recur(sugar.Subtract(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Multiply(es):
            match es:
                case []:
                    return kernel.Int(1)
                case [first, *rest]:
                    return kernel.Multiply(recur(first), recur(sugar.Multiply(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case kernel.Let(x, e1, e2):
            return kernel.Let(x, recur(e1), recur(e2))

        case kernel.Var():
            return expr

        case sugar.LetStar(bindings, body):
            match bindings:
                case []:
                    return recur(body)
                case [[x, e1], *rest]:
                    return kernel.Let(x, recur(e1), recur(sugar.LetStar(rest, body)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case kernel.Bool():
            return expr

        case sugar.Not(e1):
            return kernel.If(kernel.EqualTo(recur(e1), kernel.Bool(True)), kernel.Bool(False), kernel.Bool(True))

        case sugar.All(es):
            match es:
                case []:
                    return kernel.Bool(True)
                case [first, *rest]:
                    return kernel.If(recur(first), recur(sugar.All(rest)), kernel.Bool(False))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.Any(es):
            match es:
                case []:
                    return kernel.Bool(False)
                case [first, *rest]:
                    return kernel.If(recur(first), kernel.Bool(True), recur(sugar.Any(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case kernel.If(e1, e2, e3):
            return kernel.If(recur(e1), recur(e2), recur(e3))

        case sugar.Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return kernel.If(recur(e1), recur(e2), recur(sugar.Cond(rest, default)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.LessThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return kernel.Bool(True)
                case [first, second]:
                    return kernel.GreaterThanOrEqualTo(recur(second), recur(first))
                case [first, second, *rest]:
                    return recur(
                        sugar.All(
                            [
                                sugar.LessThanOrEqualTo([first, second]),
                                sugar.LessThanOrEqualTo([second, *rest]),
                            ]
                        )
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.LessThan(es):
            match es:
                case [] | [_]:
                    return kernel.Bool(True)
                case [first, second]:
                    return kernel.LessThan(recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(sugar.All([sugar.LessThan([first, second]), sugar.LessThan([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.EqualTo(es):
            match es:
                case [] | [_]:
                    return kernel.Bool(True)
                case [first, second]:
                    return kernel.EqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(sugar.All([sugar.EqualTo([first, second]), sugar.EqualTo([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThan(es):
            match es:
                case [] | [_]:
                    return kernel.Bool(True)
                case [first, second]:
                    return kernel.LessThan(recur(second), recur(first))
                case [first, second, *rest]:
                    return recur(sugar.All([sugar.GreaterThan([first, second]), sugar.GreaterThan([second, *rest])]))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case sugar.GreaterThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return kernel.Bool(True)
                case [first, second]:
                    return kernel.GreaterThanOrEqualTo(recur(first), recur(second))
                case [first, second, *rest]:
                    return recur(
                        sugar.All(
                            [sugar.GreaterThanOrEqualTo([first, second]), sugar.GreaterThanOrEqualTo([second, *rest])]
                        )
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()
