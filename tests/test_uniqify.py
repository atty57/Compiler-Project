import pytest
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var
from uniqify import Environment, uniqify, uniqify_expr
from util import SequentialNameGenerator


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Program, Program]](
        [
            (
                Program([], Int(0)),
                Program([], Int(0)),
            ),
            (
                Program(["x"], Var("x")),
                Program(["_x0"], Var("_x0")),
            ),
        ]
    ),
)
def test_uniqify(
    expr: Program,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Expression]](
        [
            (
                Int(0),
                {},
                Int(0),
            ),
        ]
    ),
)
def test_uniqify_expr_int(
    expr: Int,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Add, Environment, Expression]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                Add(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_add(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Subtract, Environment, Expression]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                Subtract(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_subtract(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Multiply, Environment, Expression]](
        [
            (
                Multiply(Int(1), Int(1)),
                {},
                Multiply(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expr_multiply(
    expr: Multiply,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Let, Environment, Expression]](
        [
            (
                Let("x", Int(1), Var("x")),
                {},
                Let("_x0", Int(1), Var("_x0")),
            ),
            (
                Let("x", Int(1), Let("x", Int(2), Var("x"))),
                {},
                Let("_x0", Int(1), Let("_x1", Int(2), Var("_x1"))),
            ),
        ]
    ),
)
def test_uniqify_expr_let(
    expr: Let,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Var, Environment, Expression]](
        [
            (
                Var("x"),
                {"x": "y"},
                Var("y"),
            ),
        ]
    ),
)
def test_uniqify_expr_var(
    expr: Var,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected
