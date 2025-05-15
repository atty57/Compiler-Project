import pytest
from llvmlite import ir
from lactose import Program as LProgram, Int, Var, Let, Tuple, Get, Set, Copy, Global, Add, Lambda
from lower import lower


def make_simple_program():
    return LProgram(parameters=[], body=Int(42), functions={})


def test_lower_empty_program():
    prog = make_simple_program()
    module = lower(prog)
    assert isinstance(module, ir.Module)
    # externals
    assert module.get_global("malloc") is not None
    assert module.get_global("atoi") is not None
    # entry points
    assert module.get_global("_start") is not None
    assert module.get_global("main") is not None


def test_lower_function_definition():
    func = Lambda(parameters=["x"], body=Add(Var("x"), Int(1)))
    prog = LProgram(parameters=[], body=Int(0), functions={"f": func})
    module = lower(prog)
    ffunc = module.get_global("f")
    assert isinstance(ffunc, ir.Function)
    assert len(ffunc.args) == 1


def test_lower_tuple_get_set_copy_global():
    tup = Tuple([Int(1), Int(2)])
    get_ = Get(tup, Int(1))
    set_ = Set(tup, Int(0), Int(9))
    cp = Copy(Int(7))
    gl = Global("malloc")
    for stmt in (get_, set_, cp, gl):
        prog = LProgram(parameters=[], body=stmt, functions={})
        # should not raise
        lower(prog)
