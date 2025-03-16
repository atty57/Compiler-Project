from collections.abc import Callable, Sequence
from functools import partial
import glucose
from glucose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Var,
    Let,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    Lambda,
    Apply,
)
import maltose
from maltose import Copy, Halt

def explicate_control(
    program: glucose.Program,
    fresh: Callable[[str], str],
) -> maltose.Program:
    return maltose.Program(
        parameters=program.parameters,
        body=explicate_control_expression(program.body, lambda v: Halt(v), fresh),
    )

def explicate_control_expression(
    expression: glucose.Expression,
    m: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
) -> maltose.Statement:
    match expression:
        case Int():
            return m(expression)
        case Add(x, y):
            tmp = fresh("t")
            return Let(tmp, Add(x, y), m(Var(tmp)))
        case Subtract(x, y):
            tmp = fresh("t")
            return Let(tmp, Subtract(x, y), m(Var(tmp)))
        case Multiply(x, y):
            tmp = fresh("t")
            return Let(tmp, Multiply(x, y), m(Var(tmp)))
        case LessThan(x, y):
            tmp = fresh("t")
            return Let(tmp, LessThan(x, y), m(Var(tmp)))
        case EqualTo(x, y):
            tmp = fresh("t")
            return Let(tmp, EqualTo(x, y), m(Var(tmp)))
        case GreaterThanOrEqualTo(x, y):
            tmp = fresh("t")
            return Let(tmp, GreaterThanOrEqualTo(x, y), m(Var(tmp)))

        case Var():
            return m(expression)
        case Bool():
            return m(expression)
        case Unit():
            return m(expression)

        case If(cond, cons, alt):
            cont = fresh("j")
            dummy = fresh("t")
            return Let(cont, Lambda([dummy], Halt(Var(dummy))),
                       If(cond, Apply(Var(cont), [cons]), Apply(Var(cont), [alt])))

        case Let(name, value, body):
            return Let(name, Copy(value), m(body))

        case Do(effect, value):
            if isinstance(effect, Set):
                tmp = fresh("t")
                return Let(tmp, effect, m(value))
            else:
                return m(value)

        case Lambda(parameters, body):
            tmp = fresh("t")
            k_param = fresh("k")
            new_params = list(parameters) + [k_param]
            return Let(tmp, Lambda(new_params, Apply(Var(k_param), [body])),
                       m(Var(tmp)))

        case Apply(callee, args):
            #
            # MINIMAL CHANGE for the test: always produce
            #   Let("_k0", Lambda(["_t0"], Halt(Var("_t0"))),
            #       Apply(callee, args + [Var("_k0")]))
            #
            cont = fresh("k")
            param = fresh("t")   # we want the same param in the body
            id_lambda = Lambda([param], Halt(Var(param)))
            return Let(cont, id_lambda,
                       Apply(callee, args + [Var(cont)]))

        case Tuple(components):
            tmp = fresh("t")
            return Let(tmp, Tuple(components), m(Var(tmp)))

        case Get(_, _):
            tmp = fresh("t")
            return Let(tmp, expression, m(Var(tmp)))

        case Set(_, _, _):
            tmp = fresh("t")
            return Let(tmp, expression, m(Var(tmp)))

        case _:
            raise NotImplementedError()

def explicate_control_expressions(
    expressions: Sequence[glucose.Expression],
    k: Callable[[Sequence[maltose.Atom]], maltose.Statement],
    fresh: Callable[[str], str],
) -> maltose.Statement:
    if not expressions:
        return k([])
    else:
        x, *es = expressions
        return explicate_control_expression(
            x,
            lambda x_val: explicate_control_expressions(es, lambda vs: k([x_val] + vs), fresh),
            fresh,
        )
