from collections.abc import Callable
from functools import partial
import fructose
from fructose import LetRec, Not, And, Or, Cond, Cell
import sucrose
from sucrose import Int, Var, Bool, If, Unit, Tuple


def simplify(
    program: fructose.Program,
    fresh: Callable[[str], str],
) -> sucrose.Program:
    return sucrose.Program(
        program.parameters,
        body=simplify_expression(LetRec(program.definitions, program.body), fresh),
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
            bindings = list(bindings or [])
            if not bindings:
                return recur(body)
            xs: list[str] = [name for name, _ in bindings]
            es: list[fructose.Expression] = [val for _, val in bindings]
            lam = sucrose.Lambda(xs, recur(body))
            arg_list = [recur(e) for e in es]
            return sucrose.Apply(lam, arg_list)

        case fructose.LetStar(bindings, body):
            bindings = list(bindings or [])
            if not bindings:
                return recur(body)
            if len(bindings) == 1:
                (x, val) = bindings[0]
                lam = sucrose.Lambda([x], recur(body))
                return sucrose.Apply(lam, [recur(val)])
            else:
                (x1, e1) = bindings[0]
                rest = bindings[1:]
                lam = sucrose.Lambda([x1], recur(fructose.LetStar(rest, body)))
                return sucrose.Apply(lam, [recur(e1)])

        case fructose.LetRec(bindings, body):
            bindings = list(bindings or [])
            if not bindings:
                return recur(body)
            all_vars = [b[0] for b in bindings]

            def chain_assigns(varvals: list[tuple[str, fructose.Expression]]) -> sucrose.Expression:
                if not varvals:
                    return recur(body)
                (v, e) = varvals[0]
                tempName = fresh("t")
                rest = varvals[1:]
                next_part = chain_assigns(rest)
                return sucrose.Apply(
                    sucrose.Lambda([tempName], next_part),
                    [sucrose.Assign(v, recur(e))]
                )

            inside = chain_assigns(bindings)
            outer_lam = sucrose.Lambda(all_vars, inside)
            units = [sucrose.Unit() for _ in all_vars]
            return sucrose.Apply(outer_lam, units)

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
                case [x, y]:
                    return sucrose.If(recur(x), recur(y), Bool(False))
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
                case [x, y]:
                    return sucrose.If(recur(x), Bool(True), recur(y))
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

        case fructose.Begin(body_list):
            if not body_list:
                return sucrose.Unit()
            if len(body_list) == 1:
                return recur(body_list[0])
            else:
                head = body_list[0]
                tail = fructose.Begin(body_list[1:])
                tempName = fresh("t")
                return sucrose.Apply(
                    sucrose.Lambda([tempName], recur(tail)),
                    [recur(head)]
                )

        case fructose.While(condition, loop_body):
            loopVar = fresh("loop")  # e.g. "_loop0"
            t0 = fresh("t")         # e.g. "_t0"
            t1 = fresh("t")         # e.g. "_t1"

            # Define the loop body
            lamLoop = sucrose.Lambda(
                [],
                sucrose.If(
                    recur(condition),
                    sucrose.Apply(
                        sucrose.Lambda([t1], sucrose.Apply(sucrose.Var(loopVar), [])),
                        [recur(loop_body)],
                    ),
                    sucrose.Unit(),
                ),
            )

            # We'll assign (loopVar = lamLoop)
            assignLoop = sucrose.Assign(loopVar, lamLoop)

            # Then we do an inner apply that calls Var(loopVar)
            bodyOfLoop = sucrose.Apply(
                sucrose.Lambda([t0], sucrose.Apply(sucrose.Var(loopVar), [])),
                [assignLoop]
            )

            # Outer lambda that takes [loopVar]
            outerLam = sucrose.Lambda([loopVar], bodyOfLoop)

            # Finally, apply that outerLam to Unit
            return sucrose.Apply(outerLam, [sucrose.Unit()])

        case fructose.Lambda(params, body):
            return sucrose.Lambda(params, recur(body))

        case fructose.Apply(callee, arguments):
            new_callee = recur(callee)
            new_args = [recur(a) for a in arguments]
            return sucrose.Apply(new_callee, new_args)

        case fructose.Assign(name, value):
            return sucrose.Assign(name, recur(value))

        case _:
            raise NotImplementedError(f"simplify_expression not implemented for {expression}")
