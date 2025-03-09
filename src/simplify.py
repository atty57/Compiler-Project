from collections.abc import Callable
from functools import partial
import fructose
from fructose import Let, LetStar, LetRec, Not, And, Or, Cond, Cell, Begin, While
import sucrose
from sucrose import Int, Var, Bool, If, Unit, Tuple, Lambda, Apply, Assign


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
                    raise NotImplementedError()

        case fructose.Subtract(operands):
            match operands:
                case [x]:
                    return sucrose.Subtract(Int(0), recur(x))
                case [x, y]:
                    return sucrose.Subtract(recur(x), recur(y))
                case [x, *rest]:
                    return sucrose.Subtract(recur(x), recur(fructose.Subtract(rest)))
                case _:
                    raise NotImplementedError()

        case fructose.Multiply(operands):
            match operands:
                case []:
                    return Int(1)
                case [x]:
                    return recur(x)
                case [x, *rest]:
                    return sucrose.Multiply(recur(x), recur(fructose.Multiply(rest)))
                case _:
                    raise NotImplementedError()

        case fructose.Let(bindings, body):
            if not bindings:
                return recur(body)
            xs: list[str] = []
            es: list[fructose.Expression] = []
            for name, val in bindings:
                xs.append(name)
                es.append(val)
            lam = sucrose.Lambda(xs, recur(body))
            arg_list = [recur(e) for e in es]
            return sucrose.Apply(lam, arg_list)

        case fructose.LetStar(bindings, body):
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
            if not bindings:
                return recur(body)
            all_vars = [b[0] for b in bindings]

            def chain_assigns(varvals: list[tuple[str, fructose.Expression]]) -> sucrose.Expression:
                if not varvals:
                    return recur(body)
                (v, e) = varvals[0]
                # Fresh name each time:
                tempName = fresh("t")
                rest = varvals[1:]
                next_part = chain_assigns(rest)
                return sucrose.Apply(
                    sucrose.Lambda([tempName], next_part),
                    [sucrose.Assign(v, recur(e))]
                )

            inside = chain_assigns(list(bindings))
            outer_lam = sucrose.Lambda(all_vars, inside)
            units = [sucrose.Unit() for _ in all_vars]
            return sucrose.Apply(outer_lam, units)

        case Var():
            return expression

        case Bool():
            return expression

        case Not(x):
            return If(
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
                    return If(recur(x), recur(y), Bool(False))
                case [x, *rest]:
                    return If(recur(x), recur(Or(rest)), Bool(False))
                case _:
                    raise NotImplementedError()

        case Or(operands):
            match operands:
                case []:
                    return Bool(False)
                case [x]:
                    return recur(x)
                case [x, y]:
                    return If(recur(x), Bool(True), recur(y))
                case [x, *rest]:
                    return If(recur(x), Bool(True), recur(And(rest)))
                case _:
                    raise NotImplementedError()

        case If(condition, consequent, alternative):
            return If(recur(condition), recur(consequent), recur(alternative))

        case Cond(arms, default):
            match arms:
                case []:
                    return recur(default)
                case [[e1, e2], *rest]:
                    return If(recur(e1), recur(e2), recur(Cond(rest, default)))
                case _:
                    raise NotImplementedError()

        # L E S S - T H A N - O R - E Q U A L - T O
        case fructose.LessThanOrEqualTo(es):
            match es:
                case []:
                    return Bool(True)
                case [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.GreaterThanOrEqualTo(recur(y), recur(x))
                case [x, y, *rest]:
                    return If(
                        sucrose.GreaterThanOrEqualTo(recur(y), recur(x)),
                        recur(fructose.LessThanOrEqualTo([y, *rest])),
                        Bool(False),
                    )
                case _:
                    raise NotImplementedError()

        # L E S S - T H A N
        case fructose.LessThan(es):
            match es:
                case []:
                    return Bool(True)
                case [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.LessThan(recur(x), recur(y))
                case [x, y, *rest]:
                    return If(
                        sucrose.LessThan(recur(x), recur(y)),
                        recur(fructose.LessThan([y, *rest])),
                        Bool(False),
                    )
                case _:
                    raise NotImplementedError()

        # E Q U A L - T O
        case fructose.EqualTo(es):
            match es:
                case []:
                    return Bool(True)
                case [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.EqualTo(recur(x), recur(y))
                case [x, y, *rest]:
                    return If(
                        sucrose.EqualTo(recur(x), recur(y)),
                        recur(fructose.EqualTo([y, *rest])),
                        Bool(False),
                    )
                case _:
                    raise NotImplementedError()

        # G R E A T E R - T H A N
        case fructose.GreaterThan(es):
            match es:
                case []:
                    return Bool(True)
                case [_]:
                    return Bool(True)
                case [x, y]:
                    # The spec wants "GreaterThan(x,y)" => "LessThan(y,x)"
                    return sucrose.LessThan(recur(y), recur(x))
                case [x, y, *rest]:
                    return If(
                        sucrose.LessThan(recur(y), recur(x)),
                        recur(fructose.GreaterThan([y, *rest])),
                        Bool(False),
                    )
                case _:
                    raise NotImplementedError()

        # G R E A T E R - T H A N - O R - E Q U A L - T O
        case fructose.GreaterThanOrEqualTo(es):
            match es:
                case []:
                    return Bool(True)
                case [_]:
                    return Bool(True)
                case [x, y]:
                    return sucrose.GreaterThanOrEqualTo(recur(x), recur(y))
                case [x, y, *rest]:
                    return If(
                        sucrose.GreaterThanOrEqualTo(recur(x), recur(y)),
                        recur(fructose.GreaterThanOrEqualTo([y, *rest])),
                        Bool(False),
                    )
                case _:
                    raise NotImplementedError()

        case Unit():
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
                tempName = fresh("t")   # was fresh("_t") originally
                return sucrose.Apply(
                    sucrose.Lambda([tempName], recur(tail)),
                    [recur(head)]
                )

        case fructose.While(condition, loop_body):
            loopName = fresh("loop")
            tempName0 = fresh("t")
            lamLoop = sucrose.Lambda(
                [],
                sucrose.If(
                    recur(condition),
                    sucrose.Apply(
                        sucrose.Lambda([fresh("t")], sucrose.Apply(sucrose.Var(loopName), [])),
                        [recur(loop_body)]
                    ),
                    sucrose.Unit(),
                ),
            )
            assignLoop = sucrose.Assign(loopName, lamLoop)
            step = sucrose.Apply(
                sucrose.Lambda([tempName0], sucrose.Apply(sucrose.Var(loopName), [])),
                [assignLoop]
            )
            outer = sucrose.Lambda([loopName], step)
            return sucrose.Apply(outer, [sucrose.Unit()])

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
