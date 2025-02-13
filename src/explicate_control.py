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
) -> cps.Statement:
    tail = partial(ec_tail, fresh=fresh)
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)

    match expr:
        case monadic.Int(i):
            return cps.Return(cps.Int(i))

        case monadic.Primitive(operator, a1, a2):
            return cps.Return(cps.Primitive(operator, a1, a2))

        case monadic.Var(x):
            return cps.Return(cps.Var(x))

        case monadic.Let(x, e1, e2):
            return assign(x, e1, next=tail(e2))

        case monadic.If(condition, consequent, alternative):
            return predicate(
                condition,
                then=tail(consequent),
                otherwise=tail(alternative),
            )


def ec_assign(
    dest: str,
    value: monadic.Expression,
    next: cps.Statement,
    fresh: Callable[[str], str],
) -> cps.Statement:
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)

    match value:
        case monadic.Int(i):
            return cps.Let(dest, cps.Int(i), next)

        case monadic.Primitive(operator, a1, a2):
            return cps.Let(dest, cps.Primitive(operator, a1, a2), next)

        case monadic.Var(x):
            return cps.Let(dest, cps.Var(x), next)

        case monadic.Let(x, e1, e2):
            return assign(x, e1, assign(dest, e2, next))

        case monadic.If(e1, e2, e3):
            return predicate(e1, assign(dest, e2, next), assign(dest, e3, next))


def ec_predicate(
    expr: monadic.Expression,
    then: cps.Statement,
    otherwise: cps.Statement,
    fresh: Callable[[str], str],
) -> cps.Statement:
    assign = partial(ec_assign, fresh=fresh)

    predicate = partial(ec_predicate, fresh=fresh)

    match expr:
        case monadic.Int(i):
            return otherwise if i == 0 else then

        case monadic.Primitive():
            tmp = fresh("t")
            return assign(tmp, expr, predicate(monadic.Var(tmp), then, otherwise))

        case monadic.If(e1, e2, e3):
            return predicate(e1, predicate(e2, then, otherwise), predicate(e3, then, otherwise))

        case monadic.Let(x, e1, e2):
            return assign(x, e1, next=predicate(e2, then, otherwise))

        case monadic.Var(x):
            ifTrue = fresh("b")
            ifFalse = fresh("b")
            return cps.Let(
                ifTrue,
                cps.Block(then),
                cps.Let(
                    ifFalse,
                    cps.Block(otherwise),
                    cps.Branch(x, cps.Jump(ifTrue), cps.Jump(ifFalse)),
                ),
            )
