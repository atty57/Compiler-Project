from collections.abc import Callable
from functools import partial
import monadic
import cps


def explicate_control(
    program: monadic.Program,
    fresh: Callable[[str], str],
) -> cps.Program:
    return cps.Program(
        program.parameters,
        ec_tail(program.body, fresh),
    )


def ec_tail(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
) -> cps.Tail:
    tail = partial(ec_tail, fresh=fresh)
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)
    effect = partial(ec_effect, fresh=fresh)

    match expr:
        case monadic.Int(i):
            return cps.Return(cps.Int(i))

        case monadic.Unary(operator, a1):
            return cps.Return(cps.Unary(operator, a1))

        case monadic.Binary(operator, a1, a2):
            match operator:
                case "+" | "-" | "*":
                    return cps.Return(cps.Binary(operator, a1, a2))
                case "<" | "==" | ">=":
                    return cps.Return(cps.Binary(operator, a1, a2))
                case ":=":
                    return effect(expr, cps.Return(cps.Unit()))

        case monadic.Let(x, e1, e2):
            return assign(x, e1, next=tail(e2))

        case monadic.Var(x):
            return cps.Return(cps.Var(x))

        case monadic.Bool(b):
            return cps.Return(cps.Bool(b))

        case monadic.If(e1, e2, e3):  # pragma: no branch
            return predicate(e1, then=tail(e2), otherwise=tail(e3))

        case monadic.Unit():
            return cps.Return(cps.Unit())

        case monadic.While():
            return effect(expr, cps.Return(cps.Unit()))


def ec_assign(
    dest: str,
    value: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)
    effect = partial(ec_effect, fresh=fresh)

    match value:
        case monadic.Int(i):
            return cps.Seq(cps.Assign(dest, cps.Int(i)), next)

        case monadic.Unary(operator, a1):
            return cps.Seq(cps.Assign(dest, cps.Unary(operator, a1)), next)

        case monadic.Binary(operator, a1, a2):
            match operator:
                case "+" | "-" | "*" | "<" | "==" | ">=":
                    return cps.Seq(cps.Assign(dest, cps.Binary(operator, a1, a2)), next)
                case ":=":
                    return effect(value, cps.Seq(cps.Assign(dest, cps.Unit()), next))

        case monadic.Var(x):
            return cps.Seq(cps.Assign(dest, cps.Var(x)), next)

        case monadic.Bool(b):
            return cps.Seq(cps.Assign(dest, cps.Bool(b)), next)

        case monadic.Let(x, e1, e2):
            return assign(x, e1, assign(dest, e2, next))

        case monadic.If(e1, e2, e3):
            return predicate(e1, assign(dest, e2, next), assign(dest, e3, next))

        case monadic.Unit():
            return cps.Seq(cps.Assign(dest, cps.Unit()), next)

        case monadic.While():  # pragma: no branch
            return effect(value, assign(dest, monadic.Unit(), next))


def ec_predicate(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)

    match expr:
        case monadic.Int():  # pragma: no cover
            raise ValueError()

        case monadic.Unary(operator, _):
            match operator:
                case "cell":  # pragma: no cover
                    raise ValueError()
                case "^":
                    tmp = fresh("t")
                    return assign(tmp, expr, predicate(monadic.Var(tmp), then, otherwise))

        case monadic.Binary(operator, _, _):
            match operator:
                case "+" | "-" | "*":  # pragma: no cover
                    raise ValueError()
                case "<" | "==" | ">=":
                    tmp = fresh("t")
                    return assign(tmp, expr, predicate(monadic.Var(tmp), then, otherwise))
                case ":=":  # pragma: no cover
                    raise ValueError()

        case monadic.Let(x, e1, e2):
            return assign(x, e1, next=predicate(e2, then, otherwise))

        case monadic.Var(x):
            ifTrue = fresh("then")
            ifFalse = fresh("else")
            return cps.Seq(
                cps.Assign(ifTrue, cps.Block(then)),
                cps.Seq(
                    cps.Assign(ifFalse, cps.Block(otherwise)),
                    cps.Branch(x, cps.Jump(ifTrue), cps.Jump(ifFalse)),
                ),
            )

        case monadic.Bool(b):
            match b:
                case True:
                    return then
                case False:
                    return otherwise

        case monadic.If(e1, e2, e3):
            return predicate(e1, predicate(e2, then, otherwise), predicate(e3, then, otherwise))

        case monadic.Unit():  # pragma: no cover
            raise ValueError()

        case monadic.While():  # pragma: no cover
            raise ValueError()


def ec_effect(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)
    effect = partial(ec_effect, fresh=fresh)

    match expr:
        case monadic.Int():
            return next

        case monadic.Unary(operator, _):
            return next

        case monadic.Binary(operator, a1, a2):
            match operator:
                case "+" | "-" | "*":
                    return next
                case "<" | "==" | ">=":
                    return next
                case ":=":
                    return cps.Seq(cps.Binary(operator, a1, a2), next)

        case monadic.Let(x, e1, e2):
            return assign(x, e1, effect(e2, next))

        case monadic.Var():
            return next

        case monadic.Bool():
            return next

        case monadic.If(e1, e2, e3):
            return predicate(e1, effect(e2, next), effect(e3, next))

        case monadic.Unit():
            return next

        case monadic.While(e1, e2):  # pragma: no branch
            loop = fresh("loop")
            return cps.Seq(
                cps.Assign(
                    loop,
                    cps.Block(predicate(e1, effect(e2, cps.Jump(loop)), next)),
                ),
                cps.Jump(loop),
            )
