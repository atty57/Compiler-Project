import pytest
from constant_folding import constant_fold, CompileError
from glucose import (
    Program,
    Int,
    Var,
    Bool,
    Unit,
    Add,
    Subtract,
    Multiply,
    Div,
    Let,
    If,
    Tuple,
    Get,
    Set,
    Do,
    Lambda,
    Apply,
)
from typing import Any


class Expression:
    pass


@pytest.mark.parametrize(
    "prog, expected",
    [
        # Basic arithmetic operations with constants
        (Program([], Add(Int(2), Int(3))), Int(5)),
        (Program([], Subtract(Int(5), Int(3))), Int(2)),
        (Program([], Multiply(Int(4), Int(3))), Int(12)),
        (Program([], Div(Int(6), Int(2))), Int(3)),
        # Identity operations
        (Program(["x"], Add(Var("x"), Int(0))), Var("x")),
        (Program(["x"], Add(Int(0), Var("x"))), Var("x")),
        (Program(["x"], Multiply(Var("x"), Int(1))), Var("x")),
        (Program(["x"], Multiply(Int(1), Var("x"))), Var("x")),
        (Program(["x"], Div(Var("x"), Int(1))), Var("x")),
        (Program(["x"], Subtract(Var("x"), Int(0))), Var("x")),
        # Zero multiplication
        (Program(["x"], Multiply(Var("x"), Int(0))), Int(0)),
        (Program(["x"], Multiply(Int(0), Var("x"))), Int(0)),
        # Zero division
        (Program(["x"], Div(Int(0), Var("x"))), Int(0)),
        # Nested expressions
        (Program([], Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))), Int(2)),
        # Control flow with constant conditions
        (Program([], If(Bool(True), Int(1), Int(2))), Int(1)),
        (Program([], If(Bool(False), Int(1), Int(2))), Int(2)),
        # Let bindings
        (Program([], Let("x", Add(Int(1), Int(2)), Var("x"))), Int(3)),
        # Tuple operations
        (Program([], Tuple([Int(1), Add(Int(2), Int(3))])), Tuple([Int(1), Int(5)])),
        (Program([], Get(Tuple([Int(1), Int(2)]), Int(0))), Get(Tuple([Int(1), Int(2)]), Int(0))),
        (
            Program([], Set(Tuple([Int(1), Int(2)]), Int(0), Add(Int(2), Int(3)))),
            Set(Tuple([Int(1), Int(2)]), Int(0), Int(5)),
        ),
        # Function operations
        (Program([], Lambda(["x"], Add(Int(1), Int(2)))), Lambda(["x"], Int(3))),
        (Program([], Apply(Lambda(["x"], Add(Int(1), Int(2))), [Int(0)])), Apply(Lambda(["x"], Int(3)), [Int(0)])),
        # Effects
        (Program([], Do(Add(Int(1), Int(2)), Int(3))), Do(Int(3), Int(3))),
        # Base cases
        (Program([], Int(42)), Int(42)),
        (Program(["x"], Var("x")), Var("x")),
        (Program([], Bool(True)), Bool(True)),
        (Program([], Unit()), Unit()),
    ],
)
def test_constant_folding(prog: Program, expected: Program) -> None:
    folded = constant_fold(prog)
    assert isinstance(folded.body, type(expected))
    if hasattr(expected, "value"):
        assert getattr(folded.body, "value", None) == expected.value
    if hasattr(expected, "name"):
        assert getattr(folded.body, "name", None) == expected.name


@pytest.mark.parametrize(
    "prog",
    [
        Program([], Div(Int(5), Int(0))),  # Direct division by zero
        Program([], Div(Add(Int(2), Int(3)), Subtract(Int(2), Int(2)))),  # Indirect division by zero
    ],
)
def test_constant_folding_errors(prog: Program) -> None:
    with pytest.raises(CompileError):
        constant_fold(prog)


def test_unrecognized_expression():
    class UnknownExpr(Expression):
        pass

    prog = Program([], UnknownExpr())
    result = constant_fold(prog)
    assert isinstance(result.body, UnknownExpr)
