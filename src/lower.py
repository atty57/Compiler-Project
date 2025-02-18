from collections.abc import Mapping
from functools import partial
from typing import cast
from llvmlite import ir  # type: ignore
from cps import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Var,
    Bool,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Cell,
    Get,
    Block,
    Statement,
    Assign,
    Set,
    Tail,
    Seq,
    Return,
    Jump,
    If,
)


type Environment = Mapping[str, ir.Value]


i1 = cast(ir.IntType, ir.IntType(1))
i8 = cast(ir.IntType, ir.IntType(8))
i64 = cast(ir.IntType, ir.IntType(64))


def lower(
    program: Program,
) -> ir.Module:
    module = ir.Module()

    atoi = ir.Function(module, ir.FunctionType(i64, [i8.as_pointer()]), "atoi")

    main = ir.Function(
        module,
        ir.FunctionType(i64, [i64, i8.as_pointer().as_pointer()]),
        "main",
    )
    block = main.append_basic_block()
    builder = ir.IRBuilder(block)
    _argc, argv = main.args
    env = {
        p: builder.call(atoi, [builder.load(builder.gep(argv, [ir.Constant(i64, i + 1)]))])  # type: ignore
        for i, p in enumerate(program.parameters)
    }

    lower_tail(program.body, env, builder)

    return module


def lower_tail(
    tail: Tail,
    env: Environment,
    builder: ir.IRBuilder,
) -> None:
    recur = partial(lower_tail, builder=builder)
    match tail:
        case Seq(stmt, next):
            recur(next, env=lower_stmt(stmt, env, builder))

        case Return(value):
            builder.ret(lower_expr(value, env, builder))  # type: ignore

        case Jump(target):
            builder.branch(env[target])  # type: ignore

        case If(condition, Jump(then), Jump(otherwise)):
            builder.cbranch(  # type: ignore
                builder.trunc(lower_expr(condition, env, builder), i1),  # type: ignore
                env[then],
                env[otherwise],
            )


def lower_stmt(
    stmt: Statement,
    env: Environment,
    builder: ir.IRBuilder,
) -> Environment:
    match stmt:
        case Assign(name, value):
            return {**env, name: lower_expr(value, env, builder)}

        case Set(a1, a2):
            builder.store(value=lower_expr(a2), ptr=lower_expr(a1))  # type: ignore
            return env


def lower_expr(
    expr: Expression,
    env: Environment,
    builder: ir.IRBuilder,
) -> ir.Value:
    recur = partial(lower_expr, env=env, builder=builder)

    match expr:
        case Int(i):
            return ir.Constant(i64, i)

        case Add(a1, a2):
            return builder.add(recur(a1), recur(a2))  # type: ignore

        case Subtract(a1, a2):
            return builder.sub(recur(a1), recur(a2))  # type: ignore

        case Multiply(a1, a2):
            return builder.mul(recur(a1), recur(a2))  # type: ignore

        case Var(x):
            return env[x]

        case Bool(b):
            return builder.zext(ir.Constant(i1, b), i64)  # type: ignore

        case LessThan(a1, a2):
            return builder.zext(builder.icmp_signed("<", recur(a1), recur(a2)), i64)  # type: ignore

        case EqualTo(a1, a2):
            return builder.zext(builder.icmp_signed("==", recur(a1), recur(a2)), i64)  # type: ignore

        case GreaterThanOrEqualTo(a1, a2):
            return builder.zext(builder.icmp_signed(">=", recur(a1), recur(a2)), i64)  # type: ignore

        case Unit():
            return ir.Constant(i64, 0)

        case Cell(a1):
            cell = builder.alloca(i64)  # type: ignore
            builder.store(recur(a1), ptr=cell)  # type: ignore
            return cell

        case Get(a1):
            return builder.load(ptr=recur(a1))  # type: ignore

        case Block(body):
            block: ir.Block = cast(ir.Block, builder.append_basic_block())
            lower_tail(body, env, ir.IRBuilder(block))
            return block
