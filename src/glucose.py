from collections.abc import Sequence
from dataclasses import dataclass
from typing import Union
from maltose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Tuple,
    Get,
    Set,
    Lambda,
    Apply,
)

type Expression = Union[
    Int,
    Add[Expression],
    Subtract[Expression],
    Multiply[Expression],
    Let[Expression, Expression],
    Var,
    Bool,
    If[Expression, Expression, Expression],
    LessThan[Expression],
    EqualTo[Expression],
    GreaterThanOrEqualTo[Expression],
    Unit,
    Tuple[Expression],
    Get[Expression],
    Set[Expression],
    Do[Expression, Expression],
    Lambda[Expression],
    Apply[Expression],
]


@dataclass(frozen=True)
class Do[Effect, Value]:
    effect: Effect
    value: Value


@dataclass(frozen=True)
class Program:
    parameters: Sequence[str]
    body: Expression


# def substitute_expression(
#     expression: Expression,
#     replacements: Mapping[str, Expression],
#     fresh: Callable[[str], str],
# ) -> Expression:
#     for old, new in replacements.items():
#         expression = _substitute_expression(expression, old, new, fresh)
#     return expression


# def _substitute_expression(
#     expression: Expression,
#     old: str,
#     new: Expression,
#     fresh: Callable[[str], str],
# ) -> Expression:
#     recur = partial(_substitute_expression, old=old, new=new, fresh=fresh)
#     rename = partial(rename_expression, fresh=fresh)
#     match expression:
#         case Int():
#             return expression
#         case Add(x, y):
#             return Add(recur(x), recur(y))
#         case Subtract(x, y):
#             return Subtract(recur(x), recur(y))
#         case Multiply(x, y):
#             return Multiply(recur(x), recur(y))
#         case Let(name, value, body):
#             if old == name:
#                 return Let(name, recur(value), body)

#             if name in free_variables(new):
#                 replacement = fresh(name)
#                 return Let(replacement, recur(value), recur(rename(body, {name: replacement})))
#             else:
#                 return Let(name, recur(value), recur(body))

#         case Var(x):
#             return new if old == x else expression
#         case Bool():
#             return expression
#         case If(condition, consequent, alternative):
#             return If(recur(condition), recur(consequent), recur(alternative))
#         case LessThan(x, y):
#             return LessThan(recur(x), recur(y))
#         case EqualTo(x, y):
#             return Add(recur(x), recur(y))
#         case GreaterThanOrEqualTo(x, y):
#             return Add(recur(x), recur(y))
#         case Unit():
#             return expression
#         case Tuple(components):
#             return Tuple([recur(e) for e in components])
#         case Get(tuple, index):
#             return Get(recur(tuple), recur(index))
#         case Set(tuple, index, value):
#             return Set(recur(tuple), recur(index), recur(value))
#         case Do(effect, value):
#             return Do(recur(effect), recur(value))
#         case Lambda(parameters, body):
#             if old in parameters:
#                 return expression

#             fvs = free_variables(new)
#             replacements = {parameter: fresh(parameter) for parameter in parameters if parameter in fvs}
#             return Lambda(list(replacements.values()), recur(rename(body, replacements)))

#         case Apply(callee, arguments):
#             return Apply(recur(callee), [recur(e) for e in arguments])

#         case Label(name, body):
#             if old == name:
#                 return expression

#             if name in free_variables(new):
#                 replacement = fresh(name)
#                 return Label(replacement, recur(rename(body, {name: replacement})))
#             else:
#                 return Label(name, recur(body))

#         case Jump(target, value):
#             return Jump(recur(target), recur(value))


# def free_variables(
#     expression: Expression,
# ) -> set[str]:
#     recur = partial(free_variables)

#     match expression:
#         case Int():
#             return set()

#         case Add(x, y) | Subtract(x, y) | Multiply(x, y):
#             return recur(x) | recur(y)

#         case Let(name, value, body):
#             return recur(value) | (recur(body) - {name})

#         case Var(x):
#             return {x}

#         case Bool():
#             return set()

#         case If(condition, consequent, alternative):
#             return recur(condition) | recur(consequent) | recur(alternative)

#         case LessThan(x, y) | EqualTo(x, y) | GreaterThanOrEqualTo(x, y):
#             return recur(x) | recur(y)

#         case Unit():
#             return set()

#         case Tuple(components):
#             return {fv for e in components for fv in recur(e)}

#         case Get(tuple, index):
#             return recur(tuple) | recur(index)

#         case Set(tuple, index, value):
#             return recur(tuple) | recur(index) | recur(value)

#         case Do(effect, value):
#             return recur(effect) | recur(value)

#         case Lambda(parameters, body):
#             return recur(body) - set(parameters)

#         case Apply(callee, arguments):
#             return recur(callee) | {fv for e in arguments for fv in recur(e)}

#         case Label(name, body):
#             return recur(body) - {name}

#         case Jump(target, value):  # pragma: no branch
#             return recur(target) | recur(value)


# def rename_expression(
#     expression: Expression,
#     replacements: Mapping[str, str],
#     fresh: Callable[[str], str],
# ) -> Expression:
#     return substitute_expression(
#         expression,
#         {old: Var(new) for old, new in replacements.items()},
#         fresh,
#     )
