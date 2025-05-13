import pytest

from constant_folding import constant_fold, CompileError
from glucose import Program, Int, Bool, Var, Add, Subtract, Multiply, Div


def test_div_positive():
    # 6 / 2 → 3
    prog = Program([], Div(Int(6), Int(2)))
    folded = constant_fold(prog)
    assert isinstance(folded.body, Int)
    assert folded.body.value == 3


def test_div_edge_zero_numerator():
    # 0 / x → 0  (edge)
    prog = Program(["x"], Div(Int(0), Var("x")))
    folded = constant_fold(prog)
    assert isinstance(folded.body, Int)
    assert folded.body.value == 0


def test_div_edge_unit_denominator():
    # x / 1 → x  (edge)
    prog = Program(["x"], Div(Var("x"), Int(1)))
    folded = constant_fold(prog)
    assert isinstance(folded.body, Var)
    assert folded.body.name == "x"


def test_div_negative_by_zero_literal():
    # 5 / 0 → compile‐time error  (negative)
    prog = Program([], Div(Int(5), Int(0)))
    with pytest.raises(CompileError):
        constant_fold(prog)


def test_fold_add_identities():
    # x + 0 → x ; 0 + x → x
    p1 = Program(["x"], Add(Var("x"), Int(0)))
    p2 = Program(["x"], Add(Int(0), Var("x")))
    assert isinstance(constant_fold(p1).body, Var)
    assert constant_fold(p1).body.name == "x"
    assert isinstance(constant_fold(p2).body, Var)
    assert constant_fold(p2).body.name == "x"


def test_fold_mul_identities_and_zero():
    # x * 1 → x ; 1 * x → x ; x * 0 → 0 ; 0 * x → 0
    p1 = Program(["x"], Multiply(Var("x"), Int(1)))
    p2 = Program(["x"], Multiply(Int(1), Var("x")))
    p3 = Program(["x"], Multiply(Var("x"), Int(0)))
    p4 = Program(["x"], Multiply(Int(0), Var("x")))
    assert isinstance(constant_fold(p1).body, Var) and constant_fold(p1).body.name == "x"
    assert isinstance(constant_fold(p2).body, Var) and constant_fold(p2).body.name == "x"
    assert isinstance(constant_fold(p3).body, Int) and constant_fold(p3).body.value == 0
    assert isinstance(constant_fold(p4).body, Int) and constant_fold(p4).body.value == 0


def test_fold_subtract_zero():
    # x - 0 → x
    prog = Program(["x"], Subtract(Var("x"), Int(0)))
    folded = constant_fold(prog)
    assert isinstance(folded.body, Var) and folded.body.name == "x"


def test_pipeline_constant_fold_then_vn():
    # ((3*0) + (4/2)) → ((0) + 2) → 2
    expr = Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))
    prog = Program([], expr)
    folded = constant_fold(prog)
    # after folding: Int(2)
    assert isinstance(folded.body, Int)
    assert folded.body.value == 2 