# type: ignore
from typing import cast
from llvmlite import ir, binding
from ctypes import CFUNCTYPE, POINTER, c_int32, c_int64, c_char_p

binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()

i1 = cast(ir.IntType, ir.IntType(1))
i8 = cast(ir.IntType, ir.IntType(8))
i64 = cast(ir.IntType, ir.IntType(64))


def build() -> ir.Module:
    # Create an LLVM module
    module = ir.Module()

    foo = ir.Function(
        module,
        ir.FunctionType(i64, []),
        "foo",
    )
    block = foo.append_basic_block()
    builder = ir.IRBuilder(block)
    builder.ret(ir.Constant(i64, 42))  # type: ignore

    main = ir.Function(
        module,
        ir.FunctionType(i64, []),
        "main",
    )
    block = main.append_basic_block()
    builder = ir.IRBuilder(block)

    ptr = builder.ptrtoint(foo, i64)

    builder.ret(builder.call(builder.inttoptr(ptr, ir.FunctionType(i64, []).as_pointer()), []))  # type:ignore

    return module


def execute(
    source: str,
) -> int:
    machine = binding.Target.from_default_triple().create_target_machine()
    module = binding.parse_assembly(source)
    with binding.create_mcjit_compiler(module, machine) as engine:
        engine.finalize_object()
        engine.run_static_constructors()

        f_ptr = engine.get_function_address("main")
        cfunc = CFUNCTYPE(c_int64)(f_ptr)
        return cfunc()


if __name__ == "__main__":
    module = build()
    result = execute(str(module))
    print(result)
