from collections.abc import Callable
from functools import partial
import fructose
from fructose import LetStar, LetRec, Not, And, Or, Cond, Cell, Begin, While
import sucrose
from sucrose import Int, Var, Bool, If, Unit, Tuple, Do, Lambda, Apply, Assign


def simplify(
    program: fructose.Program,
    fresh: Callable[[str], str],
) -> sucrose.Program:
    return sucrose.Program(
        program.parameters,
        body=simplify_expression(program.body, fresh),
    )


def simplify_expression(
    expression: fructose.Expression,
    fresh: Callable[[str], str],
) -> sucrose.Expression:
    recur = partial(simplify_expression, fresh=fresh)

    match expression:
        case Int():
            return expression

        case fructose.Add(operands):
            match operands:
                case []:
                    return Int(0)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.Add(recur(x), recur(fructose.Add(rest)))
                case _:
                    raise NotImplementedError(f"Add: unhandled operands: {operands}")

        case fructose.Subtract(operands):
            match operands:
                case [x]:
                    return sucrose.Subtract(Int(0), recur(x))
                case [x, y]:
                    return sucrose.Subtract(recur(x), recur(y))
                case [x, *rest]:
                    return sucrose.Subtract(recur(x), recur(fructose.Subtract(rest)))
                case _:
                    raise NotImplementedError(f"Subtract: unhandled operands: {operands}")

        case fructose.Multiply(operands):
            match operands:
                case []:
                    return Int(1)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.Multiply(recur(x), recur(fructose.Multiply(rest)))
                case _:
                    raise NotImplementedError(f"Multiply: unhandled operands: {operands}")

        case fructose.Let(bindings, body):
            match bindings:
                case []:
                    return recur(body)
                case [(name, value), *rest]:
                    return sucrose.Let(name, recur(value), recur(fructose.Let(rest, body)))
                case _:  # pragma: no cover
                    raise ValueError()

        case LetStar(bindings, body):
            match bindings:
                case []:
                    return recur(body)
                case [(name, value), *rest]:
                    return sucrose.Let(name, recur(value), recur(LetStar(rest, body)))
                case _:  # pragma: no cover
                    raise ValueError()

        case LetRec(bindings, body):
            return recur(
                fructose.Let(
                    [(name, Unit()) for name, _ in bindings],
                    Begin([*[Assign(name, value) for name, value in bindings], body]),
                ),
            )

        case Var():
            return expression

        case Bool():
            return expression

        case Not(x):
            return sucrose.If(
                sucrose.EqualTo(recur(x), Bool(True)),
                Bool(False),
                Bool(True),
            )

        case And(operands):
            match operands:
                case []:
                    return Bool(True)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.If(recur(x), recur(fructose.Or(rest)), Bool(False))
                case _:
                    raise NotImplementedError(f"And: unhandled operands: {operands}")

        case Or(operands):
            match operands:
                case []:
                    return Bool(False)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.If(recur(x), Bool(True), recur(fructose.And(rest)))
                case _:
                    raise NotImplementedError(f"Or: unhandled operands: {operands}")

        case fructose.If(condition, consequent, alternative):
            return sucrose.If(recur(condition), recur(consequent), recur(alternative))

        case Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return sucrose.If(recur(e1), recur(e2), recur(fructose.Cond(rest, default)))
                case _:
                    raise NotImplementedError(f"Cond: unhandled arms: {arms}")

        # Comparison forms with named-attribute matching for operands:
        case fructose.LessThanOrEqualTo(operands=es_seq):
            es_list: list[fructose.Expression] = list(es_seq or [])
            match es_list:
                case []:
                    return sucrose.Bool(True)
                case [_]:
                    return sucrose.Bool(True)
                case [x, y]:
                    return sucrose.GreaterThanOrEqualTo(recur(y), recur(x))
                case [x, y, *rest]:
                    rest_list: list[fructose.Expression] = [y, *rest]
                    return sucrose.If(
                        sucrose.GreaterThanOrEqualTo(recur(y), recur(x)),
                        recur(fructose.LessThanOrEqualTo(rest_list)),
                        sucrose.Bool(False),
                    )
                case _:
                    raise NotImplementedError(f"LessThanOrEqualTo: unhandled operands: {es_list}")

        case fructose.LessThan(operands=es_seq):
            es_list: list[fructose.Expression] = list(es_seq or [])
            match es_list:
                case []:
                    return sucrose.Bool(True)
                case [_]:
                    return sucrose.Bool(True)
                case [x, y]:
                    return sucrose.LessThan(recur(x), recur(y))
                case [x, y, *rest]:
                    rest_list: list[fructose.Expression] = [y, *rest]
                    return sucrose.If(
                        sucrose.LessThan(recur(x), recur(y)),
                        recur(fructose.LessThan(rest_list)),
                        sucrose.Bool(False),
                    )
                case _:
                    raise NotImplementedError(f"LessThan: unhandled operands: {es_list}")

        case fructose.EqualTo(operands=es_seq):
            es_list: list[fructose.Expression] = list(es_seq or [])
            match es_list:
                case []:
                    return sucrose.Bool(True)
                case [_]:
                    return sucrose.Bool(True)
                case [x, y]:
                    return sucrose.EqualTo(recur(x), recur(y))
                case [x, y, *rest]:
                    rest_list: list[fructose.Expression] = [y, *rest]
                    return sucrose.If(
                        sucrose.EqualTo(recur(x), recur(y)),
                        recur(fructose.EqualTo(rest_list)),
                        sucrose.Bool(False),
                    )
                case _:
                    raise NotImplementedError(f"EqualTo: unhandled operands: {es_list}")

        case fructose.GreaterThan(operands=es_seq):
            es_list: list[fructose.Expression] = list(es_seq or [])
            match es_list:
                case []:
                    return sucrose.Bool(True)
                case [_]:
                    return sucrose.Bool(True)
                case [x, y]:
                    return sucrose.LessThan(recur(y), recur(x))
                case [x, y, *rest]:
                    rest_list: list[fructose.Expression] = [y, *rest]
                    return sucrose.If(
                        sucrose.LessThan(recur(y), recur(x)),
                        recur(fructose.GreaterThan(rest_list)),
                        sucrose.Bool(False),
                    )
                case _:
                    raise NotImplementedError(f"GreaterThan: unhandled operands: {es_list}")

        case fructose.GreaterThanOrEqualTo(operands=es_seq):
            es_list: list[fructose.Expression] = list(es_seq or [])
            match es_list:
                case []:
                    return sucrose.Bool(True)
                case [_]:
                    return sucrose.Bool(True)
                case [x, y]:
                    return sucrose.GreaterThanOrEqualTo(recur(x), recur(y))
                case [x, y, *rest]:
                    rest_list: list[fructose.Expression] = [y, *rest]
                    return sucrose.If(
                        sucrose.GreaterThanOrEqualTo(recur(x), recur(y)),
                        recur(fructose.GreaterThanOrEqualTo(rest_list)),
                        sucrose.Bool(False),
                    )
                case _:
                    raise NotImplementedError(f"GreaterThanOrEqualTo: unhandled operands: {es_list}")

        case fructose.Unit():
            return expression

        case Cell(value):
            return Tuple([recur(value)])

        case fructose.Get(cell):
            return sucrose.Get(recur(cell), Int(0))

        case fructose.Set(cell, value):
            return sucrose.Set(recur(cell), Int(0), recur(value))

        case fructose.Begin(body):
            match body:
                case []:
                    return Unit()
                case [value]:
                    return recur(value)
                case [first, *rest]:
                    return Do(recur(first), recur(Begin(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case While(condition, body):
            loop = fresh("loop")
            return recur(
                LetRec(
                    [(loop, Lambda([], If(condition, Begin([body, Apply(Var(loop), [])]), Unit())))],
                    Apply(Var(loop), []),
                )
            )

        case Lambda(parameters, body):
            return Lambda(parameters, recur(body))

        case Apply(callee, arguments):
            return Apply(recur(callee), [recur(argument) for argument in arguments])

        case Assign(name, value):  # pragma: no branch
            return Assign(name, recur(value))
