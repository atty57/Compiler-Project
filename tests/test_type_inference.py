import pytest
from fructose import *
from type_inference import infer_types, TypeError, IntType, BoolType, UnitType
from type_inference import FunType, TypeVar, unify


def test_int():
    prog = Program([], Int(42))
    types = infer_types(prog)
    assert types["$result"] == IntType()


def test_bool():
    prog = Program([], Bool(True))
    types = infer_types(prog)
    assert types["$result"] == BoolType()


def test_unit():
    prog = Program([], Unit())
    types = infer_types(prog)
    assert types["$result"] == UnitType()


def test_add():
    prog = Program([], Add([Int(1), Int(2)]))
    types = infer_types(prog)
    assert types["$result"] == IntType()


def test_and():
    prog = Program([], And([Bool(True), Bool(False)]))
    types = infer_types(prog)
    assert types["$result"] == BoolType()


def test_if():
    prog = Program([], If(Bool(True), Int(1), Int(2)))
    types = infer_types(prog)
    assert types["$result"] == IntType()


def test_if_type_error():
    prog = Program([], If(Int(1), Int(1), Int(2)))
    with pytest.raises(TypeError):
        infer_types(prog)


def test_let():
    prog = Program([], Let([("x", Int(1))], Add([Var("x"), Int(2)])))
    types = infer_types(prog)
    assert types["$result"] == IntType()


def test_let_shadow():
    prog = Program([], Let([("x", Int(1))], Let([("x", Bool(True))], Var("x"))))
    types = infer_types(prog)
    assert types["$result"] == BoolType()


def test_apply_type_error():
    lam = Lambda(["x"], Add([Var("x"), Int(1)]))
    prog = Program([], Apply(lam, [Bool(True)]))
    with pytest.raises(TypeError):
        infer_types(prog)


def test_unbound_var():
    prog = Program([], Var("x"))
    with pytest.raises(TypeError):
        infer_types(prog)


def test_recursive_type_error():
    # let x = x in x
    prog = Program([], Let([("x", Var("x"))], Var("x")))
    with pytest.raises(TypeError):
        infer_types(prog)


def test_cond():
    prog = Program([], Cond([(Bool(True), Int(1)), (Bool(False), Int(2))], Int(3)))
    types = infer_types(prog)
    assert types["$result"] == IntType()


def test_while():
    prog = Program([], While(Bool(True), Int(1)))
    types = infer_types(prog)
    assert types["$result"] == UnitType()
