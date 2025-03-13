from collections.abc import Mapping
from functools import partial
from typing import cast
from llvmlite import ir  #  type: ignore
from lactose import (
    Program,
    Atom,
    Int,
    Var,
    Bool,
    Unit,
    Expression,
    Add,
    Subtract,
    Multiply,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Copy,
    Global,
    Statement,
    Let,
    Apply,
    If,
    Halt,
)

i1 = cast(ir.IntType, ir.IntType(1))
i8 = cast(ir.IntType, ir.IntType(8))
i64 = cast(ir.IntType, ir.IntType(64))


def lower(
    program: Program,
) -> ir.Module:
    module = ir.Module()

    ir.Function(module, ir.FunctionType(i64.as_pointer(), [i64]), "malloc")

    atoi = ir.Function(module, ir.FunctionType(i64, [i8.as_pointer()]), "atoi")

    for name, abs in program.functions.items():
        fun = ir.Function(module, ir.FunctionType(i64, [i64 for _ in abs.parameters]), name)  # type: ignore
        fun.calling_convention = "tailcc"
        env = {p: v for p, v in zip(abs.parameters, fun.args, strict=True)}
        lower_statement(abs.body, env, ir.IRBuilder(fun.append_basic_block()))

    start = ir.Function(module, ir.FunctionType(i64, [i64 for _ in program.parameters]), "_start")  # type: ignore
    start.calling_convention = "tailcc"
    env = {p: a for p, a in zip(program.parameters, start.args, strict=True)}
    lower_statement(program.body, env, ir.IRBuilder(start.append_basic_block()))

    main = ir.Function(module, ir.FunctionType(i64, [i64, i8.as_pointer().as_pointer()]), "main")
    builder = ir.IRBuilder(main.append_basic_block())
    _argc, argv = main.args
    builder.ret(  # type:ignore
        builder.call(  # type:ignore
            start,
            [
                builder.call(atoi, [builder.load(builder.gep(argv, [ir.Constant(i64, i + 1)]))])  # type: ignore
                for i, _ in enumerate(program.parameters)
            ],
        )
    )

    return module


def lower_statement(
    statement: Statement,
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> None:
    atom = partial(lower_atom, env=env, builder=builder)
    recur = partial(lower_statement, env=env, builder=builder)
    expr = partial(lower_expression, env=env, builder=builder)

    match statement:
        case _:
            raise NotImplementedError()


def lower_expression(
    expression: Expression,
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> ir.Value:
    atom = partial(lower_atom, env=env, builder=builder)

    match expression:
        case _:
            raise NotImplementedError()


def lower_atom(
    atom: Atom,
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> ir.Value:
    match atom:
        case _:
            raise NotImplementedError()
