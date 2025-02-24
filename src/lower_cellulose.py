from collections.abc import Mapping, MutableMapping
from functools import partial
from typing import cast
from llvmlite import ir  # type: ignore
from cellulose import (
    Program,
    Function,
    Block,
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
    Tuple,
    Get,
    Apply,
    Statement,
    Assign,
    Set,
    Tail,
    Do,
    Return,
    Jump,
    If,
)


i1 = cast(ir.IntType, ir.IntType(1))
i8 = cast(ir.IntType, ir.IntType(8))
i64 = cast(ir.IntType, ir.IntType(64))


def lower(
    program: Program,
) -> ir.Module:
    module = ir.Module()

    atoi = ir.Function(module, ir.FunctionType(i64, [i8.as_pointer()]), "atoi")

    funMap: Mapping[str, ir.Function] = {
        function.name: ir.Function(module, ir.FunctionType(i64, [i64 for _ in function.parameters]), function.name)
        for function in program.functions
    }

    for function in program.functions:
        lower_function(function, funMap)

    main = ir.Function(
        module,
        ir.FunctionType(i64, [i64, i8.as_pointer().as_pointer()]),
        "main",
    )
    block = main.append_basic_block()
    blockMap: Mapping[str, ir.Block] = {"entry": block}
    builder = ir.IRBuilder(block)
    _argc, argv = main.args
    varMap: MutableMapping[str, ir.Value] = {
        p: builder.call(atoi, [builder.load(builder.gep(argv, [ir.Constant(i64, i + 1)]))])  # type: ignore
        for i, p in enumerate(program.parameters)
    }

    lower_tail(program.body, varMap, blockMap, funMap, builder)

    return module


def lower_function(
    function: Function,
    funMap: Mapping[str, ir.Function],
) -> None:
    f = funMap[function.name]
    blockMap: Mapping[str, ir.Block] = {block.name: f.append_basic_block(block.name) for block in function.blocks}
    varMap: MutableMapping[str, ir.Value] = {p: v for p, v in zip(function.parameters, f.args)}

    for block in function.blocks:
        lower_block(block, varMap, blockMap, funMap)


def lower_block(
    block: Block,
    varMap: MutableMapping[str, ir.Value],
    blockMap: Mapping[str, ir.Block],
    funMap: Mapping[str, ir.Function],
) -> None:
    b = blockMap[block.name]
    builder = ir.IRBuilder(b)
    lower_tail(block.body, varMap, blockMap, funMap, builder)


def lower_tail(
    tail: Tail,
    varMap: MutableMapping[str, ir.Value],
    blockMap: Mapping[str, ir.Block],
    funMap: Mapping[str, ir.Function],
    builder: ir.IRBuilder,
) -> None:
    recur = partial(lower_tail, varMap=varMap, blockMap=blockMap, funMap=funMap, builder=builder)
    statement = partial(lower_statement, varMap=varMap, blockMap=blockMap, funMap=funMap, builder=builder)
    expression = partial(lower_expression, varMap=varMap, blockMap=blockMap, funMap=funMap, builder=builder)

    match tail:
        case Do(stmt, next):
            statement(stmt)
            recur(next)

        case Return(value):
            builder.ret(expression(value))  # type: ignore

        case Jump(target):
            builder.branch(blockMap[target])  # type: ignore

        case If(condition, Jump(then), Jump(otherwise)):
            builder.cbranch(  # type: ignore
                builder.trunc(expression(condition), i1),  # type: ignore
                blockMap[then],
                blockMap[otherwise],
            )


def lower_statement(
    stmt: Statement,
    varMap: MutableMapping[str, ir.Value],
    blockMap: Mapping[str, ir.Block],
    funMap: Mapping[str, ir.Function],
    builder: ir.IRBuilder,
) -> None:
    expression = partial(lower_expression, varMap=varMap, blockMap=blockMap, funMap=funMap, builder=builder)
    match stmt:
        case Assign(x, e1):
            varMap[x] = expression(e1)

        case Set(a1, i, a2):
            builder.store(  # type:ignore
                expression(a2),
                ptr=builder.gep(  # type:ignore
                    builder.inttoptr(expression(a1), i64.as_pointer()),  # type:ignore
                    [ir.Constant(i64, i)],
                ),
            )  # type: ignore

        case Apply():
            expression(stmt)


def lower_expression(
    expr: Expression,
    varMap: MutableMapping[str, ir.Value],
    blockMap: Mapping[str, ir.Block],
    funMap: Mapping[str, ir.Function],
    builder: ir.IRBuilder,
) -> ir.Value:
    recur = partial(lower_expression, varMap=varMap, blockMap=blockMap, funMap=funMap, builder=builder)

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
            return varMap[x]

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

        case Tuple(as_):
            base = builder.alloca(i64, len(as_))  # type: ignore
            for i, a in enumerate(as_):
                builder.store(recur(a), builder.gep(base, [ir.Constant(i64, i)]))  # type: ignore
            return builder.ptrtoint(base, i64)  # type: ignore

        case Get(a1, i):
            base = builder.inttoptr(recur(a1), i64.as_pointer())  # type: ignore
            return builder.load(builder.gep(base, [ir.Constant(i64, i)]))  # type: ignore

        case Apply(a1, as_):
            return builder.call(  # type: ignore
                builder.inttoptr(  # type: ignore
                    recur(a1),
                    ir.FunctionType(i64, [i64 for _ in as_]).as_pointer(),
                ),
                [recur(a) for a in as_],
            )
