import pytest
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var, Bool, If, Compare
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
            # Int
            (
                Int(0),
                {},
                Int(0),
            ),
            # Add
            (
                Add(Int(1), Int(1)),
                {},
                Add(Int(1), Int(1)),
            ),
            # Subtract
            (
                Subtract(Int(1), Int(1)),
                {},
                Subtract(Int(1), Int(1)),
            ),
            # Multiply
            (
                Multiply(Int(1), Int(2)),
                {},
                Multiply(Int(1), Int(2)),
            ),
            # Let
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
            # Var
            (
                Var("x"),
                {"x": "y"},
                Var("y"),
            ),
            (
                If(Int(1), Int(2), Int(2)),
                {},
                If(Int(1), Int(2), Int(2)),
            ),
        ]
    ),
)
def test_uniqify_expr(
    expr: Expression,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


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


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Bool, Environment, Expression]](
        [
            (
                Bool(True),
                {},
                Bool(True),
            ),
        ]
    ),
)
def test_uniqify_expr_bool(
    expr: Bool,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[If, Environment, Expression]](
        [
            (
                If(Bool(True), Int(2), Int(2)),
                {},
                If(Bool(True), Int(2), Int(2)),
            ),
        ]
    ),
)
def test_uniqify_expr_if(
    expr: If,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Compare, Environment, Expression]](
        [
            (
                Compare("==", Int(0), Int(0)),
                {},
                Compare("==", Int(0), Int(0)),
            ),
        ]
    ),
)
def test_uniqify_expr_compare(
    expr: Compare,
    env: Environment,
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expr(expr, env, fresh) == expected
