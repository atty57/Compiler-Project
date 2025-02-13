from collections.abc import Sequence
import pytest
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var
from eval import Value, Environment, eval, eval_expr


@pytest.mark.parametrize(
    "program, arguments, expected",
    list[tuple[Program, Sequence[Value], Value]](
        [
            # Int
            (
                Program([], Int(0)),
                [],
                0,
            ),
            (
                Program(["x"], Var("x")),
                [0],
                0,
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
                0,
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
    list[tuple[Add, Environment, Value]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                2,
            ),
        ]
    ),
)
def test_eval_expr_add(
    expr: Add,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Subtract, Environment, Value]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                0,
            ),
        ]
    ),
)
def test_eval_expr_subtract(
    expr: Subtract,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Multiply, Environment, Value]](
        [
            (
                Multiply(Int(1), Int(2)),
                {},
                2,
            ),
        ]
    ),
)
def test_eval_multiply(
    expr: Multiply,
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
                1,
            ),
        ]
    ),
)
def test_eval_expr_let(
    expr: Let,
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
                {"x": 0},
                0,
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
