from collections.abc import Callable
from functools import partial
import monadic
from monadic import Int, Add, Subtract, Multiply, Let, Var, Bool, If, LessThan, EqualTo, GreaterThanOrEqualTo
import cps
from cps import Block, Assign, Seq, Return, Jump, Branch


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

    match expr:
        case Int() | monadic.Add() | monadic.Subtract() | monadic.Multiply():
            return Return(expr)

        case Let(x, e1, e2):
            return assign(x, e1, next=tail(e2))

        case Var():
            return Return(expr)

        case Bool():
            return Return(expr)

        case If(e1, e2, e3):
            return predicate(e1, then=tail(e2), otherwise=tail(e3))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():  # pragma: no branch
            return Return(expr)


def ec_assign(
    dest: str,
    value: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)

    match value:
        case Int():
            return Seq(Assign(dest, value), next)

        case Add() | Subtract() | Multiply():
            return Seq(Assign(dest, value), next)

        case Var():
            return Seq(Assign(dest, value), next)

        case Bool():
            return Seq(Assign(dest, value), next)

        case Let(x, e1, e2):
            return assign(x, e1, assign(dest, e2, next))

        case If(e1, e2, e3):
            return predicate(e1, assign(dest, e2, next), assign(dest, e3, next))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():  # pragma: no branch
            return Return(value)


def ec_predicate(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> cps.Tail:
    assign = partial(ec_assign, fresh=fresh)
    predicate = partial(ec_predicate, fresh=fresh)

    match expr:
        case Int() | Add() | Subtract() | Multiply():  # pragma: no cover
            raise ValueError()

        case Let(x, e1, e2):
            return assign(x, e1, next=predicate(e2, then, otherwise))

        case Var(x):
            ifTrue = fresh("then")
            ifFalse = fresh("else")
            return Seq(
                Assign(ifTrue, Block(then)),
                Seq(
                    Assign(ifFalse, Block(otherwise)),
                    Branch(x, Jump(ifTrue), Jump(ifFalse)),
                ),
            )

        case Bool(b):
            match b:
                case True:
                    return then
                case False:
                    return otherwise

        case If(e1, e2, e3):
            return predicate(e1, predicate(e2, then, otherwise), predicate(e3, then, otherwise))

        case LessThan() | EqualTo() | GreaterThanOrEqualTo():  # pragma: no branch
            tmp = fresh("t")
            return assign(tmp, expr, predicate(Var(tmp), then, otherwise))


# def ec_effect(
#     expr: monadic.Expression,
#     next: cps.Tail,
#     fresh: Callable[[str], str],
# ) -> cps.Tail:
#     assign = partial(ec_assign, fresh=fresh)
#     predicate = partial(ec_predicate, fresh=fresh)
#     effect = partial(ec_effect, fresh=fresh)

#     match expr:
#         case monadic.Int():
#             return next

#         case monadic.Unary(operator, _):
#             return next

#         case monadic.Binary(operator, a1, a2):
#             match operator:
#                 case "+" | "-" | "*":
#                     return next
#                 case "<" | "==" | ">=":
#                     return next
#                 case ":=":
#                     return cps.Seq(cps.Binary(operator, a1, a2), next)

#         case monadic.Let(x, e1, e2):
#             return assign(x, e1, effect(e2, next))

#         case monadic.Var():
#             return next

#         case monadic.Bool():
#             return next

#         case monadic.If(e1, e2, e3):
#             return predicate(e1, effect(e2, next), effect(e3, next))

#         case monadic.Unit():
#             return next

#         case monadic.While(e1, e2):  # pragma: no branch
#             loop = fresh("loop")
#             return cps.Seq(
#                 cps.Assign(
#                     loop,
#                     cps.Block(predicate(e1, effect(e2, cps.Jump(loop)), next)),
#                 ),
#                 cps.Jump(loop),
#             )
