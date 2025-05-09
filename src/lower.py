# lower.py
from collections.abc import Mapping
from functools import partial
from typing import cast
from llvmlite import ir  # type: ignore

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
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Copy,
    Global,
)

# Our target types: 1-bit for booleans and 64-bit for everything else.
i1 = ir.IntType(1)
i64 = ir.IntType(64)


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
    # A simple implementation: lower the expression and return its value.
    result = lower_expression(statement, env, builder)
    builder.ret(result)


def lower_expression(
    expression: Expression,
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> ir.Value:
    # If the expression is an Atom, lower it directly.
    if isinstance(expression, Atom):
        return lower_atom(expression, env, builder)

    match expression:
        case Add(x, y):
            v1 = lower_atom(x, env, builder)
            v2 = lower_atom(y, env, builder)
            add_result = builder.add(v1, v2, name="addtmp")
            return cast(ir.Value, add_result)

        case Subtract(x, y):
            v1 = lower_atom(x, env, builder)
            v2 = lower_atom(y, env, builder)
            sub_result = builder.sub(v1, v2, name="subtmp")
            return cast(ir.Value, sub_result)

        case Multiply(x, y):
            v1 = lower_atom(x, env, builder)
            v2 = lower_atom(y, env, builder)
            mult_result = builder.mul(v1, v2, name="multmp")
            return cast(ir.Value, mult_result)

        case LessThan(x, y):
            v1 = lower_atom(x, env, builder)
            v2 = lower_atom(y, env, builder)
            cmp = builder.icmp_signed("<", v1, v2, name="lttmp")
            return cast(ir.Value, builder.zext(cmp, i64, name="booltmp"))

        case EqualTo(x, y):
            v1 = lower_atom(x, env, builder)
            v2 = lower_atom(y, env, builder)
            cmp = builder.icmp_signed("==", v1, v2, name="eqtmp")
            return cast(ir.Value, builder.zext(cmp, i64, name="booltmp"))

        case GreaterThanOrEqualTo(x, y):
            v1 = lower_atom(x, env, builder)
            v2 = lower_atom(y, env, builder)
            cmp = builder.icmp_signed(">=", v1, v2, name="geqtmp")
            return cast(ir.Value, builder.zext(cmp, i64, name="booltmp"))

        case Let(name, value, body):
            # Lower the 'value' and bind it in the environment.
            v = lower_expression(value, env, builder)
            new_env = env.copy()
            new_env[name] = v
            return lower_expression(body, new_env, builder)

        case If(cond, then_expr, else_expr):
            # Lower the condition and convert to i1.
            cond_val = lower_expression(cond, env, builder)
            bool_cond = builder.trunc(cond_val, i1, name="ifcond")

            # Create basic blocks for then, else, and merge.
            function = builder.function
            then_bb = function.append_basic_block("then")
            else_bb = function.append_basic_block("else")
            merge_bb = function.append_basic_block("ifcont")

            builder.cbranch(bool_cond, then_bb, else_bb)

            # Then block
            builder.position_at_end(then_bb)
            then_val = lower_expression(then_expr, env, builder)
            builder.branch(merge_bb)
            then_bb = builder.block  # Capture then block.

            # Else block
            builder.position_at_end(else_bb)
            else_val = lower_expression(else_expr, env, builder)
            builder.branch(merge_bb)
            else_bb = builder.block  # Capture else block.

            # Merge block with a φ–node.
            builder.position_at_end(merge_bb)
            phi = builder.phi(i64, name="iftmp")
            phi.add_incoming(then_val, then_bb)
            phi.add_incoming(else_val, else_bb)
            return phi

        case Tuple(components):
            # Allocate memory for the tuple.
            n = len(components)
            size = ir.Constant(i64, n * 8)  # each element is 8 bytes.
            # Retrieve our externally-declared malloc; note we get it from the module.
            malloc_fn = builder.function.module.get_global("malloc")
            alloc_ptr = builder.call(malloc_fn, [size], name="tuplealloc")
            # Store each component into the allocated memory.
            for idx, comp in enumerate(components):
                comp_val = lower_atom(comp, env, builder)
                ptr = builder.gep(alloc_ptr, [ir.Constant(i64, idx)], inbounds=True, name=f"gep{idx}")
                builder.store(comp_val, ptr)
            # Convert the pointer (i64*) to an i64 integer.
            return builder.ptrtoint(alloc_ptr, i64, name="tupleint")

        case Get(tuple_expr, index_expr):
            # Lower the tuple expression, which is stored as an integer representing a pointer.
            tup_int = lower_atom(tuple_expr, env, builder)
            tup_ptr = builder.inttoptr(tup_int, i64.as_pointer(), name="tupptr")
            # Lower the index.
            idx = lower_atom(index_expr, env, builder)
            gep = builder.gep(tup_ptr, [idx], inbounds=True, name="getgep")
            return builder.load(gep, name="gettmp")

        case Set(tuple_expr, index_expr, value_expr):
            # Lower the tuple expression and index.
            tup_int = lower_atom(tuple_expr, env, builder)
            tup_ptr = builder.inttoptr(tup_int, i64.as_pointer(), name="tupptr")
            idx = lower_atom(index_expr, env, builder)
            gep = builder.gep(tup_ptr, [idx], inbounds=True, name="setgep")
            # Lower the value and store it.
            val = lower_expression(value_expr, env, builder)
            builder.store(val, gep)
            # For simplicity, have the set expression return the stored value.
            return val

        case _:
            raise NotImplementedError(f"lower_expression: unhandled expression: {expression}")


def lower_atom(
    atom: Atom,
    env: Mapping[str, ir.Value],
    builder: ir.IRBuilder,
) -> ir.Value:
    match atom:
        case Int():
            return ir.Constant(i64, atom.value)
        case Bool():
            # Create an i1 constant then zero-extend it to i64.
            b = ir.Constant(i1, 1 if atom.value else 0)
            return builder.zext(b, i64, name="boolext")
        case Var():
            try:
                return env[atom.name]
            except KeyError:
                raise NameError(f"Undefined variable: {atom.name}")
        case Unit():
            # Represent unit as 0.
            return ir.Constant(i64, 0)
        case Global():
            # Look up the global by name in the module.
            g = builder.function.module.get_global(atom.name)
            # Convert the pointer (if g is a function) to an integer.
            return builder.ptrtoint(g, i64, name="globint")
        case Copy():
            return lower_atom(atom.value, env, builder)
        case _:
            raise NotImplementedError(f"lower_atom: unhandled atom: {atom}")
