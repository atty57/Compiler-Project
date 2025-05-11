import pytest

from constant_folding import constant_fold, CompileError
from value_numbering import value_numbering, VNError
from glucose import Program, Int, Bool, Var, Add, Subtract, Multiply, Div, Let, Expression
from typing import cast

# ─── Safe Division & Constant‐Fold Tests ─────────────────────────────────────


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


# ─── Value‐Numbering Tests ────────────────────────────────────────────────────


def test_vn_simple_expression():
    # let v0 = (x + y) in v0
    body = Add(Var("x"), Var("y"))
    prog = Program(["x", "y"], body)
    vn = value_numbering(prog)
    # After VN, body must be a Let binding
    assert hasattr(vn.body, "name") and vn.body.name.startswith("v")
    assert isinstance(vn.body.value, Add)
    assert isinstance(vn.body.body, Var)
    assert vn.body.body.name == vn.body.name


def test_vn_duplicate_literals():
    # (2+3) and (2+3) → only one global binding
    expr = Add(Add(Int(2), Int(3)), Add(Int(2), Int(3)))
    prog = Program([], expr)
    vn = value_numbering(prog)
    # The first binding should be named v0
    let1 = vn.body
    assert let1.name == "v0"
    # The body of v0’s Let should be the top-level Add(...)
    assert isinstance(let1.value, Add)
    # And the final body must be Var('v0')
    assert isinstance(let1.body, Var) and let1.body.name == "v0"


def test_vn_error_on_unrecognized():
    # Passing a Bool (which VN doesn’t handle) should error
    prog = Program([], Bool(True))
    with pytest.raises(VNError):
        value_numbering(prog)


# ─── Combined Pipeline Tests ─────────────────────────────────────────────────


def test_pipeline_constant_fold_then_vn():
    # ((3*0) + (4/2)) → ((0) + 2) → let v0=2 in v0
    expr = Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))
    prog = Program([], expr)
    folded = constant_fold(prog)
    # after folding: 0 + 2
    assert isinstance(folded.body, Add)
    assert isinstance(folded.body.left, Int) and folded.body.left.value == 0
    assert isinstance(folded.body.right, Int) and folded.body.right.value == 2

    vn = value_numbering(folded)
    # after VN: let v0 = Add(Int(0), Int(2)) in v0
    let1 = vn.body
    assert isinstance(let1, type(folded.body)) is False  # it's a Let, not an Add
    assert let1.name.startswith("v")
    assert isinstance(let1.value, Add)
    assert isinstance(let1.body, Var) and let1.body.name == let1.name
