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
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.Subtract(operands):
            match operands:
                case [x]:
                    return sucrose.Subtract(Int(0), recur(x))
                case [x, y]:
                    return sucrose.Subtract(recur(x), recur(y))
                case [x, *rest]:
                    return sucrose.Subtract(recur(x), recur(fructose.Subtract(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.Multiply(operands):
            match operands:
                case []:
                    return Int(1)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.Multiply(recur(x), recur(fructose.Multiply(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

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
                    fructose.Begin([*[Assign(name, value) for name, value in bindings], body]),
                ),
            )

        case Var():
            return expression

        case Bool():
            return expression

        case Not(x):
            return If(sucrose.EqualTo(recur(x), Bool(True)), Bool(False), Bool(True))

        case And(operands):
            match operands:
                case []:
                    return Bool(True)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return If(recur(x), recur(Or(rest)), Bool(False))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Or(operands):
            match operands:
                case []:
                    return Bool(False)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return If(recur(x), Bool(True), recur(And(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case If(condition, consequent, alternative):
            return If(recur(condition), recur(consequent), recur(alternative))

        case Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return If(recur(e1), recur(e2), recur(Cond(rest, default)))
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.LessThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.GreaterThanOrEqualTo(recur(y), recur(x))
                case [x, y, *rest]:
                    return If(
                        sucrose.GreaterThanOrEqualTo(recur(y), recur(x)),
                        recur(fructose.LessThanOrEqualTo([y, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.LessThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.LessThan(recur(x), recur(y))
                case [x, y, *rest]:
                    return If(
                        sucrose.LessThan(recur(x), recur(y)),
                        recur(fructose.LessThan([y, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.EqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.EqualTo(recur(x), recur(y))
                case [x, y, *rest]:
                    return If(
                        sucrose.EqualTo(recur(x), recur(y)),
                        recur(fructose.EqualTo([y, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.GreaterThan(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.LessThan(recur(y), recur(x))
                case [x, y, *rest]:
                    return If(
                        sucrose.LessThan(recur(y), recur(x)),
                        recur(fructose.GreaterThan([y, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case fructose.GreaterThanOrEqualTo(es):
            match es:
                case [] | [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.GreaterThanOrEqualTo(recur(x), recur(y))
                case [x, y, *rest]:
                    return If(
                        sucrose.GreaterThanOrEqualTo(recur(x), recur(y)),
                        recur(fructose.GreaterThanOrEqualTo([y, *rest])),
                        Bool(False),
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError()

        case Unit():
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
            return Apply(recur(callee), [recur(e) for e in arguments])

        case Assign(name, value):  # pragma: no branch
            return Assign(name, recur(value))
