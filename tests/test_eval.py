from collections.abc import Sequence
import pytest
from kernel import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
)
from eval import Value, Environment, eval, eval_expr


@pytest.mark.parametrize(
    "program, arguments, expected",
    list[tuple[Program, Sequence[Value], Value]](
        [
            (
                Program([], Int(0)),
                [],
                Int(0),
            ),
            (
                Program(["x"], Var("x")),
                [Int(0)],
                Int(0),
            ),
        ]
    ),
)
def test_eval(
    program: Program,
    arguments: Sequence[Value],
    expected: Value,
) -> None:
    assert eval(program, arguments) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Int, Environment, Value]](
        [
            (
                Int(0),
                {},
                Int(0),
            ),
        ]
    ),
)
def test_eval_expr_int(
    expr: Int,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                Int(2),
            ),
        ]
    ),
)
def test_eval_expr_add(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                Int(0),
            ),
        ]
    ),
)
def test_eval_expr_subtract(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                Multiply(Int(1), Int(2)),
                {},
                Int(2),
            ),
        ]
    ),
)
def test_eval_multiply(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                Let("x", Int(1), Var("x")),
                {},
                Int(1),
            ),
        ]
    ),
)
def test_eval_expr_let(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Var, Environment, Value]](
        [
            (
                Var("x"),
                {"x": Int(0)},
                Int(0),
            ),
        ]
    ),
)
def test_eval_expr_var(
    expr: Var,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Bool, Environment, Value]](
        [
            (
                Bool(True),
                {},
                Bool(True),
            ),
            (
                Bool(False),
                {},
                Bool(False),
            ),
        ]
    ),
)
def test_eval_expr_bool(
    expr: Bool,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                If(Bool(True), Int(10), Int(20)),
                {},
                Int(10),
            ),
            (
                If(Bool(False), Int(10), Int(20)),
                {},
                Int(20),
            ),
            (
                If(LessThan(Int(1), Int(2)), If(Bool(False), Int(30), Int(40)), Int(50)),
                {},
                Int(40),
            ),
        ]
    ),
)
def test_eval_expr_if(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                LessThan(Int(1), Int(2)),
                {},
                Bool(True),
            ),
            (
                LessThan(Int(5), Int(3)),
                {},
                Bool(False),
            ),
            (
                LessThan(Int(5), Int(5)),
                {},
                Bool(False),
            ),
        ]
    ),
)
def test_eval_expr_less_than(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                EqualTo(Int(1), Int(2)),
                {},
                Bool(False),
            ),
            (
                EqualTo(Bool(True), Bool(True)),
                {},
                Bool(True),
            ),
            (
                EqualTo(Int(3), Int(3)),
                {},
                Bool(True),
            ),
            (
                EqualTo(Bool(True), Bool(False)),
                {},
                Bool(False),
            ),
        ]
    ),
)
def test_eval_expr_equal_to(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            (
                GreaterThanOrEqualTo(Int(2), Int(1)),
                {},
                Bool(True),
            ),
            (
                GreaterThanOrEqualTo(Int(3), Int(5)),
                {},
                Bool(False),
            ),
            (
                GreaterThanOrEqualTo(Int(5), Int(5)),
                {},
                Bool(True),
            ),
        ]
    ),
)
def test_eval_expr_greater_than_or_equal_to(
    expr: Expression,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


def test_eval_undefined_var():
    with pytest.raises(KeyError, match=r"Undefined variable: x"):
        eval_expr(Var("x"), {})
