from collections.abc import Callable
from functools import partial
import fructose
from fructose import LetStar, LetRec, Not, And, Or, Cond, Cell, Begin, While, Match, Expression
import sucrose
from sucrose import Int, Var, Bool, If, Unit, Tuple, Do, Lambda, Apply, Assign
from typing import Any


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
                    raise NotImplementedError(f"Add: unhandled operands: {operands}")

        case fructose.Subtract(operands):
            match operands:
                case [x]:
                    return sucrose.Subtract(Int(0), recur(x))
                case [x, y]:
                    return sucrose.Subtract(recur(x), recur(y))
                case [x, *rest]:
                    return sucrose.Subtract(recur(x), recur(fructose.Subtract(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError(f"Subtract: unhandled operands: {operands}")

        case fructose.Multiply(operands):
            match operands:
                case []:
                    return Int(1)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.Multiply(recur(x), recur(fructose.Multiply(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError(f"Multiply: unhandled operands: {operands}")

        case fructose.Div(operands):
            match operands:
                case []:
                    return Int(1)
                case [x]:
                    return recur(x)
                case [x, y]:
                    return sucrose.Div(recur(x), recur(y))
                case [x, *rest]:
                    return sucrose.Div(recur(x), recur(fructose.Div(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError(f"Div: unhandled operands: {operands}")

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
                case _:  # pragma: no cover
                    raise NotImplementedError(f"And: unhandled operands: {operands}")

        case Or(operands):
            match operands:
                case []:
                    return Bool(False)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.If(recur(x), Bool(True), recur(fructose.And(rest)))
                case _:  # pragma: no cover
                    raise NotImplementedError(f"Or: unhandled operands: {operands}")

        case fructose.If(condition, consequent, alternative):
            return sucrose.If(recur(condition), recur(consequent), recur(alternative))

        case Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return sucrose.If(recur(e1), recur(e2), recur(fructose.Cond(rest, default)))
                case _:  # pragma: no cover
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
                case _:  # pragma: no cover
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
                case _:  # pragma: no cover
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
                case _:  # pragma: no cover
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
                case _:  # pragma: no cover
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
                case _:  # pragma: no cover         
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

        case Match() as match_expr:
            expr, arms = match_expr.expr, match_expr.arms

            def lower_arm(arms: list[tuple[Any, Any]]) -> sucrose.Expression:
                if not arms:
                    # No match: error or unit
                    return sucrose.Unit()
                pat, body = arms[0]
                rest = arms[1:]
                # Pattern matching logic
                match pat:
                    case fructose.PatternInt(v):
                        cond = sucrose.EqualTo(recur(expr), sucrose.Int(v))
                        return sucrose.If(cond, recur(body), lower_arm(rest))
                    case fructose.PatternTrue():
                        cond = sucrose.EqualTo(recur(expr), sucrose.Bool(True))
                        return sucrose.If(cond, recur(body), lower_arm(rest))
                    case fructose.PatternFalse():
                        cond = sucrose.EqualTo(recur(expr), sucrose.Bool(False))
                        return sucrose.If(cond, recur(body), lower_arm(rest))
                    case fructose.PatternUnit():
                        cond = sucrose.EqualTo(recur(expr), sucrose.Unit())
                        return sucrose.If(cond, recur(body), lower_arm(rest))
                    case fructose.PatternVar(name):
                        # Bind variable to value and evaluate body
                        return sucrose.Let(name, recur(expr), recur(body))
                    case fructose.PatternWildcard():
                        return recur(body)
                    case fructose.PatternCons(constructor, subpatterns):
                        # Only handling tuple patterns for now
                        if constructor == "tuple":
                            # Destructure expr into its components
                            tuple_var = fresh("tuple")
                            lets = []
                            for i, _ in enumerate(subpatterns):
                                elem_var = fresh(f"elem{i}")
                                lets.append((elem_var, sucrose.Get(recur(expr), sucrose.Int(i))))

                            # Recursively match subpatterns
                            def nest_patterns(subs, lets, body):
                                if not subs:
                                    return recur(body)
                                subpat, *rest_subs = subs
                                let_name, let_val = lets[0]
                                rest_lets = lets[1:]
                                # Recursively match subpattern
                                return lower_arm([(subpat, nest_patterns(rest_subs, rest_lets, body))])

                            # Build let bindings for tuple elements
                            let_expr = recur(expr)
                            for name, val in reversed(lets):
                                let_expr = sucrose.Let(name, val, let_expr)
                            # Now match subpatterns
                            return sucrose.Let(tuple_var, recur(expr), nest_patterns(subpatterns, lets, body))
                        else:
                            raise NotImplementedError(f"Constructor pattern not supported: {constructor}")
                    case _:  # pragma: no cover
                        raise NotImplementedError(f"Pattern not supported: {pat}")

            return lower_arm(arms)
