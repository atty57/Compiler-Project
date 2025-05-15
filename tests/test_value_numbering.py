import pytest
from value_numbering import value_numbering, VNError
from glucose import Program, Int, Bool, Var, Add, Subtract, Multiply, Div, Let, If, Tuple, Get, Set, Do, Lambda, Apply
from typing import Any


@pytest.mark.parametrize(  # type: ignore
    "prog, check",
    [
        (
            Program(["x", "y"], Add(Var("x"), Var("y"))),  # type: ignore
            lambda vn: (
                hasattr(vn.body, "name")
                and vn.body.name.startswith("v")  # type: ignore
                and isinstance(vn.body.value, Add)  # type: ignore
                and hasattr(vn.body.body, "name")  # type: ignore
                and vn.body.body.name == vn.body.name  # type: ignore
            ),  # type: ignore
        ),
        (
            Program([], Add(Add(Int(2), Int(3)), Add(Int(2), Int(3)))),  # type: ignore
            lambda vn: (
                hasattr(vn.body, "name")
                and vn.body.name == "v0"  # type: ignore
                and isinstance(vn.body.value, Add)  # type: ignore
                and hasattr(vn.body.body, "name")  # type: ignore
                and vn.body.body.name == "v0"  # type: ignore
            ),  # type: ignore
        ),
    ],
)
def test_value_numbering(prog: Any, check: Any) -> None:  # type: ignore
    vn = value_numbering(prog)
    assert check(vn)


def test_vn_error_on_unrecognized() -> None:
    prog = Program([], Bool(True))
    with pytest.raises(VNError):
        value_numbering(prog)


def test_pipeline_constant_fold_then_vn() -> None:
    from constant_folding import constant_fold
    from glucose import Multiply, Div

    expr = Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))  # type: ignore
    prog = Program([], expr)
    folded = constant_fold(prog)
    vn = value_numbering(folded)
    if isinstance(vn.body, Int):
        assert vn.body.value == 2
    else:
        assert hasattr(vn.body, "name")
        assert isinstance(vn.body.value, Int) and vn.body.value.value == 2  # type: ignore
        child = getattr(vn.body, "body", None)
        assert child is not None and hasattr(child, "name")
        assert child.name == vn.body.name  # type: ignore


def test_hash_expr_all_cases():
    # Each case in _hash_expr
    env = {}
    assert "Int:1" == __import__('value_numbering')._hash_expr(Int(1), env)
    assert "Var:x" == __import__('value_numbering')._hash_expr(Var("x"), env)
    assert "Add(Int:1,Int:2)" == __import__('value_numbering')._hash_expr(Add(Int(1), Int(2)), env)
    assert "Sub(Int:1,Int:2)" == __import__('value_numbering')._hash_expr(Subtract(Int(1), Int(2)), env)
    assert "Mul(Int:1,Int:2)" == __import__('value_numbering')._hash_expr(Multiply(Int(1), Int(2)), env)
    assert "Div(Int:1,Int:2)" == __import__('value_numbering')._hash_expr(Div(Int(1), Int(2)), env)
    assert "If(Int:1;Int:2;Int:3)" == __import__('value_numbering')._hash_expr(If(Int(1), Int(2), Int(3)), env)
    assert "Let(x=Int:1;Int:2)" == __import__('value_numbering')._hash_expr(Let("x", Int(1), Int(2)), env)
    assert "Bool:True" == __import__('value_numbering')._hash_expr(Bool(True), env)
    assert "Bool:False" == __import__('value_numbering')._hash_expr(Bool(False), env)
    assert "Tup(Int:1,Int:2)" == __import__('value_numbering')._hash_expr(Tuple([Int(1), Int(2)]), env)
    assert "Get(Int:1;Int:2)" == __import__('value_numbering')._hash_expr(Get(Int(1), Int(2)), env)
    assert "Set(Int:1;Int:2;Int:3)" == __import__('value_numbering')._hash_expr(Set(Int(1), Int(2), Int(3)), env)
    assert "Do(Int:1;Int:2)" == __import__('value_numbering')._hash_expr(Do(Int(1), Int(2)), env)
    assert "Lam(x;Int:1)" == __import__('value_numbering')._hash_expr(Lambda(["x"], Int(1)), env)
    assert "App(Int:1,Int:2)" == __import__('value_numbering')._hash_expr(Apply(Int(1), [Int(2)]), env)
    # Error case
    class Dummy: pass
    with pytest.raises(__import__('value_numbering').VNError):
        __import__('value_numbering')._hash_expr(Dummy(), env)


def test_rebuild_all_cases():
    # Each case in _rebuild
    rec = lambda x: x
    assert Add(Int(1), Int(2)) == __import__('value_numbering')._rebuild(Add(Int(1), Int(2)), rec)
    assert Multiply(Int(1), Int(2)) == __import__('value_numbering')._rebuild(Multiply(Int(1), Int(2)), rec)
    assert Div(Int(1), Int(2)) == __import__('value_numbering')._rebuild(Div(Int(1), Int(2)), rec)
    assert Let("x", Int(1), Int(2)) == __import__('value_numbering')._rebuild(Let("x", Int(1), Int(2)), rec)
    assert If(Int(1), Int(2), Int(3)) == __import__('value_numbering')._rebuild(If(Int(1), Int(2), Int(3)), rec)
    assert Tuple([Int(1), Int(2)]) == __import__('value_numbering')._rebuild(Tuple([Int(1), Int(2)]), rec)
    assert Get(Int(1), Int(2)) == __import__('value_numbering')._rebuild(Get(Int(1), Int(2)), rec)
    assert Set(Int(1), Int(2), Int(3)) == __import__('value_numbering')._rebuild(Set(Int(1), Int(2), Int(3)), rec)
    assert Do(Int(1), Int(2)) == __import__('value_numbering')._rebuild(Do(Int(1), Int(2)), rec)
    assert Lambda(["x"], Int(1)) == __import__('value_numbering')._rebuild(Lambda(["x"], Int(1)), rec)
    assert Apply(Int(1), [Int(2)]) == __import__('value_numbering')._rebuild(Apply(Int(1), [Int(2)]), rec)
    assert Int(1) == __import__('value_numbering')._rebuild(Int(1), rec)
    assert Var("x") == __import__('value_numbering')._rebuild(Var("x"), rec)
    assert Bool(True) == __import__('value_numbering')._rebuild(Bool(True), rec)
    # Error case
    class Dummy: pass
    with pytest.raises(__import__('value_numbering').VNError):
        __import__('value_numbering')._rebuild(Dummy(), rec)
