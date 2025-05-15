import pytest

from constant_folding import constant_fold, CompileError
from glucose import Program, Int, Var, Add, Subtract, Multiply, Div


@pytest.mark.parametrize(
    "prog, expected",
    [
        (Program([], Div(Int(6), Int(2))), Int(3)),
        (Program(["x"], Div(Int(0), Var("x"))), Int(0)),
        (Program(["x"], Div(Var("x"), Int(1))), Var("x")),
        (Program(["x"], Add(Var("x"), Int(0))), Var("x")),
        (Program(["x"], Add(Int(0), Var("x"))), Var("x")),
        (Program(["x"], Multiply(Var("x"), Int(1))), Var("x")),
        (Program(["x"], Multiply(Int(1), Var("x"))), Var("x")),
        (Program(["x"], Multiply(Var("x"), Int(0))), Int(0)),
        (Program(["x"], Multiply(Int(0), Var("x"))), Int(0)),
        (Program(["x"], Subtract(Var("x"), Int(0))), Var("x")),
        (Program([], Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))), Int(2)),
    ],
)
def test_constant_folding(prog, expected):
    folded = constant_fold(prog)
    assert isinstance(folded.body, type(expected))
    if hasattr(expected, "value"):
        assert getattr(folded.body, "value", None) == expected.value
    if hasattr(expected, "name"):
        assert getattr(folded.body, "name", None) == expected.name


@pytest.mark.parametrize(
    "prog",
    [
        Program([], Div(Int(5), Int(0))),
    ],
)
def test_constant_folding_errors(prog):
    with pytest.raises(CompileError):
        constant_fold(prog)
