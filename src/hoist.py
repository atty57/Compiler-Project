from collections.abc import Callable, Mapping
from functools import partial
import maltose
from maltose import Lambda, Let, If, Apply, Halt
import lactose
from lactose import Global

def hoist(
    program: maltose.Program,
    fresh: Callable[[str], str],
) -> lactose.Program:
    body, functions = hoist_statement(program.body, fresh)
    return lactose.Program(
        parameters=program.parameters,
        body=body,
        functions=functions,
    )

def hoist_statement(
    statement: maltose.Statement,
    fresh: Callable[[str], str],
) -> tuple[lactose.Statement, Mapping[str, Lambda[lactose.Statement]]]:
    match statement:
        case Let(var, value, body):
            if isinstance(value, Lambda):
                # Preserve the original let–variable name.
                if var.startswith("_"):
                    var = var.lstrip("_")
                new_name = fresh("f")  # e.g. "_f0"
                body_closed, funcs = hoist_statement(body, fresh)
                return (Let(var, Global(new_name), body_closed),
                        {**funcs, new_name: value})
            else:
                body_closed, funcs = hoist_statement(body, fresh)
                return (Let(var, value, body_closed), funcs)
        case If(cond, then_stmt, else_stmt):
            then_closed, funcs_then = hoist_statement(then_stmt, fresh)
            else_closed, funcs_else = hoist_statement(else_stmt, fresh)
            return (If(cond, then_closed, else_closed), {**funcs_then, **funcs_else})
        case Apply(callee, args):
            return (Apply(callee, args), {})
        case Halt(value):
            return (Halt(value), {})
        case _:
            raise NotImplementedError()
