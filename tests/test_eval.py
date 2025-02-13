from collections.abc import Sequence
import pytest
from kernel import (
    Program,
    Expression,
    Int,
    Binary,
    Let,
    Var,
    Bool,
    If,
    Unit,
    Cell,
    CellGet,
    CellSet,
)
from eval import Value, Environment, eval, eval_expr


@pytest.mark.parametrize(
    "program, arguments, expected",
    list[tuple[Program, Sequence[Value], Value]](
        [
            # Int
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
    list[tuple[Binary, Environment, Value]](
        [
            (
                Binary("+", Int(1), Int(1)),
                {},
                Int(2),
            ),
        ]
    ),
)
def test_eval_expr_int_add(
    expr: Binary,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Binary, Environment, Value]](
        [
            (
                Binary("-", Int(1), Int(1)),
                {},
                Int(0),
            ),
        ]
    ),
)
def test_eval_expr_int_subtract(
    expr: Binary,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Binary, Environment, Value]](
        [
            (
                Binary("*", Int(1), Int(2)),
                {},
                Int(2),
            ),
        ]
    ),
)
def test_eval_int_multiply(
    expr: Binary,
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
    list[tuple[If, Environment, Value]](
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
        ]
    ),
)
def test_eval_expr_if(
    expr: If,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Binary, Environment, Value]](
        [
            (
                Binary("<", Int(1), Int(2)),
                {},
                Bool(True),
            ),
        ]
    ),
)
def test_eval_expr_less_than(
    expr: Binary,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Binary, Environment, Value]](
        [
            (
                Binary("==", Int(1), Int(2)),
                {},
                Bool(False),
            ),
            (
                Binary("==", Bool(True), Bool(True)),
                {},
                Bool(True),
            ),
        ]
    ),
)
def test_eval_expr_equal_to(
    expr: Binary,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Binary, Environment, Value]](
        [
            (
                Binary(">=", Int(2), Int(1)),
                {},
                Bool(True),
            ),
        ]
    ),
)
def test_eval_expr_greater_than_or_equal_to(
    expr: Binary,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Unit, Environment, Value]](
        [
            (
                Unit(),
                {},
                Unit(),
            ),
        ]
    ),
)
def test_eval_expr_unit(
    expr: Unit,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Cell, Environment, Value]](
        [
            (
                Cell(Int(0)),
                {},
                True,
            ),
        ]
    ),
)
def test_eval_expr_cell(
    expr: Cell,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_expr(expr, env) == expected
