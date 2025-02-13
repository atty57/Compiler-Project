import pytest
from kernel import Program, Expression, Int, Binary, Let, Var, Bool, If
from opt import opt, opt_expr


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[Program, Program]](
        [
            (
                Program([], Int(0)),
                Program([], Int(0)),
            ),
        ]
    ),
)
def test_opt(
    program: Program,
    expected: Program,
) -> None:
    assert opt(program) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Int, Expression]](
        [
            (
                Int(0),
                Int(0),
            ),
        ]
    ),
)
def test_opt_expr_int(
    expr: Int,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Binary, Expression]](
        [
            (
                Binary("+", Int(0), Var("x")),
                Var("x"),
            ),
            (
                Binary("+", Var("x"), Int(0)),
                Var("x"),
            ),
            (
                Binary("+", Int(1), Int(1)),
                Int(2),
            ),
            (
                Binary("+", Int(1), Binary("+", Int(1), Int(1))),
                Int(3),
            ),
            (
                Binary("+", Int(1), Binary("+", Var("x"), Int(1))),
                Binary("+", Int(2), Var("x")),
            ),
            (
                Binary("+", Binary("+", Int(1), Var("x")), Binary("+", Int(1), Var("y"))),
                Binary("+", Int(2), Binary("+", Var("x"), Var("y"))),
            ),
            (
                Binary("+", Int(1), Binary("+", Int(1), Var("x"))),
                Binary("+", Int(2), Var("x")),
            ),
            (
                Binary("+", Int(1), Var("x")),
                Binary("+", Int(1), Var("x")),
            ),
            (
                Binary("+", Var("x"), Int(1)),
                Binary("+", Int(1), Var("x")),
            ),
            (
                Binary("+", Var("x"), Var("y")),
                Binary("+", Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_add(
    expr: Binary,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Binary, Expression]](
        [
            (
                Binary("-", Int(2), Int(1)),
                Int(1),
            ),
            (
                Binary("-", Var("x"), Var("y")),
                Binary("-", Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_subtract(
    expr: Binary,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Binary, Expression]](
        [
            (
                Binary("*", Int(0), Var("x")),
                Int(0),
            ),
            (
                Binary("*", Var("x"), Int(0)),
                Int(0),
            ),
            (
                Binary("*", Int(1), Var("x")),
                Var("x"),
            ),
            (
                Binary("*", Var("x"), Int(1)),
                Var("x"),
            ),
            (
                Binary("*", Int(1), Int(2)),
                Int(2),
            ),
            (
                Binary("*", Int(1), Binary("*", Int(2), Int(3))),
                Int(6),
            ),
            (
                Binary("*", Int(2), Binary("*", Var("x"), Int(3))),
                Binary("*", Int(6), Var("x")),
            ),
            (
                Binary("*", Binary("*", Int(2), Var("x")), Binary("*", Int(3), Var("y"))),
                Binary("*", Int(6), Binary("*", Var("x"), Var("y"))),
            ),
            (
                Binary("*", Int(2), Binary("*", Int(3), Var("x"))),
                Binary("*", Int(6), Var("x")),
            ),
            (
                Binary("*", Int(2), Var("x")),
                Binary("*", Int(2), Var("x")),
            ),
            (
                Binary("*", Var("x"), Int(2)),
                Binary("*", Int(2), Var("x")),
            ),
            (
                Binary("*", Var("x"), Var("y")),
                Binary("*", Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_multiply(
    expr: Binary,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Let, Expression]](
        [
            (
                Let("x", Int(1), Var("x")),
                Int(1),
            ),
            (
                Let("x", Int(1), Var("y")),
                Let("x", Int(1), Var("y")),
            ),
        ]
    ),
)
def test_opt_expr_let(
    expr: Let,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Var, Expression]](
        [
            (
                Var("x"),
                Var("x"),
            ),
        ]
    ),
)
def test_opt_expr_var(
    expr: Var,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Bool, Expression]](
        [
            (
                Bool(True),
                Bool(True),
            ),
            (
                Bool(False),
                Bool(False),
            ),
        ]
    ),
)
def test_opt_expr_bool(
    expr: Bool,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[If, Expression]](
        [
            (
                If(Bool(True), Int(0), Int(1)),
                Int(0),
            ),
            (
                If(Bool(False), Int(0), Int(1)),
                Int(1),
            ),
            (
                If(Var("x"), Int(0), Int(1)),
                If(Var("x"), Int(0), Int(1)),
            ),
        ]
    ),
)
def test_opt_expr_if(
    expr: If,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Binary, Expression]](
        [
            (
                Binary("<", Int(0), Int(1)),
                Bool(True),
            ),
            (
                Binary("<", Int(0), Var("x")),
                Binary("<", Int(0), Var("x")),
            ),
        ]
    ),
)
def test_opt_expr_less_than(
    expr: Binary,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Binary, Expression]](
        [
            (
                Binary("==", Int(0), Int(1)),
                Bool(False),
            ),
            (
                Binary("==", Bool(True), Bool(True)),
                Bool(True),
            ),
            (
                Binary("==", Int(1), Var("x")),
                Binary("==", Int(1), Var("x")),
            ),
        ]
    ),
)
def test_opt_expr_equal_to(
    expr: Binary,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Binary, Expression]](
        [
            (
                Binary(">=", Int(0), Int(1)),
                Bool(False),
            ),
            (
                Binary(">=", Int(1), Var("x")),
                Binary(">=", Int(1), Var("x")),
            ),
        ]
    ),
)
def test_opt_expr_greeater_than_or_equal_to(
    expr: Binary,
    expected: Expression,
) -> None:
    assert opt_expr(expr) == expected
