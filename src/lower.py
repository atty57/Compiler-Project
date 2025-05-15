from collections.abc import Mapping
from functools import partial
from llvmlite import ir  # type:ignore

from lactose import (
    Program,
    Atom,
    Expression,
    Int,
    Var,
    Bool,
    Add,
    Subtract,
    Multiply,
    Div,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Copy,
    Global,
    Unit,
    Let,
    If,
    Apply,
    Halt,
)

# Our target types: 1-bit for booleans and 64-bit for everything else.
i1: ir.IntType = ir.IntType(1)
i64: ir.IntType = ir.IntType(64)


def lower(
    program: Program,
) -> ir.Module:
    module = ir.Module()

    # Declare external functions.
    ir.Function(module, ir.FunctionType(i64.as_pointer(), [i64]), "malloc")
    atoi = ir.Function(module, ir.FunctionType(i64, [ir.IntType(8).as_pointer()]), "atoi")

    # Lower each defined function in the program.
    for name, abs in program.functions.items():
        fun = ir.Function(module, ir.FunctionType(i64, [i64 for _ in abs.parameters]), name)  # type: ignore
        fun.calling_convention = "tailcc"
        env = {p: v for p, v in zip(abs.parameters, fun.args, strict=True)}
        lower_statement(abs.body, env, ir.IRBuilder(fun.append_basic_block()))

    # Lower the main program body.
    start = ir.Function(module, ir.FunctionType(i64, [i64 for _ in program.parameters]), "_start")  # type: ignore
    start.calling_convention = "tailcc"
    env = {p: a for p, a in zip(program.parameters, start.args, strict=True)}
    lower_statement(program.body, env, ir.IRBuilder(start.append_basic_block()))

    main = ir.Function(module, ir.FunctionType(i64, [i64, ir.IntType(8).as_pointer().as_pointer()]), "main")
    builder = ir.IRBuilder(main.append_basic_block())
    _argc, argv = main.args
    builder.ret(  # type:ignore
        builder.call(  # type:ignore
            start,
            [
                builder.call(atoi, [builder.load(builder.gep(argv, [ir.Constant(i64, i + 1)]))])
                for i, _ in enumerate(program.parameters)
            ],
        )
    )
    return module


def lower_statement(
    statement: Expression,  # In our uniform representation our body is an expression.
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> None:
    atom = partial(lower_atom, env=env, builder=builder)
    recur = partial(lower_statement, env=env, builder=builder)
    expr = partial(lower_expression, env=env, builder=builder)

    match statement:
        case Let(name, value, next):
            return recur(next, env={**env, name: expr(value)})

        case If(condition, then, otherwise):
            with builder.if_else(builder.trunc(atom(condition), i1)) as (
                ifTrue,
                ifFalse,
            ):  # type: ignore
                with ifTrue:
                    recur(then)
                with ifFalse:
                    recur(otherwise)
            builder.unreachable()

        case Apply(callee, arguments):
            builder.ret(  # type: ignore
                builder.call(  # type: ignore
                    fn=builder.inttoptr(  # type: ignore
                        atom(callee),
                        ir.FunctionType(i64, [i64 for _ in arguments]).as_pointer(),
                    ),
                    args=[atom(argument) for argument in arguments],
                    tail="musttail",  # type: ignore
                    cconv="tailcc",
                )
            )

        case Halt(value):  # pragma: no branch
            builder.ret(atom(value))  # type: ignore
        case _:
            pass


def lower_expression(
    expression: Expression,
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> ir.Value:
    # If the expression is an Atom, lower it directly.
    if isinstance(expression, (Int, Var, Bool, Unit)):
        return lower_atom(expression, env, builder)
    atom = partial(lower_atom, env=env, builder=builder)

    match expression:
        case Add(x, y):
            return builder.add(atom(x), atom(y))  # type: ignore

        case Subtract(x, y):
            return builder.sub(atom(x), atom(y))  # type: ignore

        case Multiply(x, y):
            return builder.mul(atom(x), atom(y))  # type: ignore

        case Div(x, y):
            return builder.sdiv(atom(x), atom(y))  # type: ignore

        case LessThan(x, y):
            return builder.zext(builder.icmp_signed("<", atom(x), atom(y)), typ=i64)  # type: ignore

        case EqualTo(x, y):
            return builder.zext(builder.icmp_signed("==", atom(x), atom(y)), typ=i64)  # type: ignore

        case GreaterThanOrEqualTo(x, y):
            return builder.zext(builder.icmp_signed(">=", atom(x), atom(y)), typ=i64)  # type: ignore

        case Tuple(xs):
            base = builder.call(builder.module.get_global("malloc"), [ir.Constant(i64, len(xs) * 8)])  # type: ignore

            for i, x in enumerate(xs):
                builder.store(value=atom(x), ptr=builder.gep(base, [ir.Constant(i64, i)]))  # type: ignore

            return builder.ptrtoint(base, typ=i64)  # type: ignore

        case Get(base, index):
            # Cast the integer base address to a pointer of type i64
            cast_ptr = builder.inttoptr(atom(base), i64.as_pointer(), "cast_ptr")
            # Compute the address of the desired element with inbounds GEP
            gep_ptr = builder.gep(cast_ptr, [atom(index)], inbounds=True, source_etype=i64)
            # Load the value with explicit type
            return builder.load(gep_ptr, name="load_val", typ=i64)  # type: ignore

        case Set(base, index, value):
            builder.store(  # type: ignore
                atom(value),
                builder.gep(builder.inttoptr(atom(base), i64.as_pointer()), [atom(index)]),  # type: ignore
            )
            return ir.Constant(i64, 0)

        case Copy(value):
            return atom(value)

        case Global(name):
            return builder.ptrtoint(builder.module.get_global(name), typ=i64)  # type: ignore


def lower_atom(
    atom: Atom,
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> ir.Value:
    match atom:
        case Int(i):
            return ir.Constant(i64, i)

        case Var(name):
            return env[name]

        case Bool(b):
            return builder.zext(ir.Constant(i1, b), typ=i64)  # type: ignore

        case Unit():
            return ir.Constant(i64, 0)
