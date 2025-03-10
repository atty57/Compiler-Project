# type: ignore
from collections.abc import Sequence
from llvmlite import binding
from ctypes import CFUNCTYPE, POINTER, c_int32, c_char_p

binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()


def execute(
    source: str,
    args: Sequence[str],
) -> int:
    machine = binding.Target.from_default_triple().create_target_machine()
    module = binding.parse_assembly(source)
    module.verify()

    with binding.create_mcjit_compiler(module, machine) as engine:
        engine.finalize_object()
        engine.run_static_constructors()

        argc = len(args) + 1
        argv = (c_char_p * argc)(*[a.encode() for a in ["program", *args]])

        f_ptr = engine.get_function_address("main")
        cfunc = CFUNCTYPE(c_int32, c_int32, POINTER(c_char_p))(f_ptr)
        return cfunc(argc, argv)
