import pytest
import sugar
import kernel
from desugar import desugar, desugar_expr


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[sugar.Program, kernel.Program]](
        [
            (
                sugar.Program([], sugar.Int(0)),
                kernel.Program([], kernel.Int(0)),
            ),
        ]
    ),
)
def test_desugar(
    program: sugar.Program,
    expected: kernel.Expression,
) -> None:
    assert desugar(program) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Int, kernel.Expression]](
        [
            (
                sugar.Int(0),
                kernel.Int(0),
            ),
        ]
    ),
)
def test_desugar_expr_int(
    expr: sugar.Int,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Add, kernel.Expression]](
        [
            (
                sugar.Add([]),
                kernel.Int(0),
            ),
            (
                sugar.Add([sugar.Int(1)]),
                kernel.Binary("+", kernel.Int(1), kernel.Int(0)),
            ),
            (
                sugar.Add([sugar.Int(1), sugar.Int(1)]),
                kernel.Binary("+", kernel.Int(1), kernel.Binary("+", kernel.Int(1), kernel.Int(0))),
            ),
        ]
    ),
)
def test_desugar_expr_int_add(
    expr: sugar.Add,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Subtract, kernel.Expression]](
        [
            (
                sugar.Subtract([sugar.Int(1)]),
                kernel.Binary("-", kernel.Int(0), kernel.Int(1)),
            ),
            (
                sugar.Subtract([sugar.Int(2), sugar.Int(1)]),
                kernel.Binary("-", kernel.Int(2), kernel.Int(1)),
            ),
            (
                sugar.Subtract([sugar.Int(3), sugar.Int(2), sugar.Int(1)]),
                kernel.Binary("-", kernel.Int(3), kernel.Binary("-", kernel.Int(2), kernel.Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_int_subtract(
    expr: sugar.Subtract,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Multiply, kernel.Expression]](
        [
            (
                sugar.Multiply([]),
                kernel.Int(1),
            ),
            (
                sugar.Multiply([sugar.Int(1)]),
                kernel.Binary("*", kernel.Int(1), kernel.Int(1)),
            ),
            (
                sugar.Multiply([sugar.Int(2), sugar.Int(2)]),
                kernel.Binary("*", kernel.Int(2), kernel.Binary("*", kernel.Int(2), kernel.Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_int_multiply(
    expr: sugar.Multiply,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Let, kernel.Expression]](
        [
            (
                sugar.Let("x", sugar.Int(0), sugar.Var("x")),
                kernel.Let("x", kernel.Int(0), kernel.Var("x")),
            ),
        ]
    ),
)
def test_desugar_expr_let(
    expr: sugar.Let,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Var, kernel.Expression]](
        [
            (
                sugar.Var("x"),
                kernel.Var("x"),
            ),
        ]
    ),
)
def test_desugar_expr_var(
    expr: sugar.Var,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Bool, kernel.Expression]](
        [
            (
                sugar.Bool(True),
                kernel.Bool(True),
            ),
        ]
    ),
)
def test_desugar_expr_bool(
    expr: sugar.Var,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Not, kernel.Expression]](
        [
            (
                sugar.Not(sugar.Var("x")),
                kernel.If(
                    kernel.Binary("==", kernel.Var("x"), kernel.Bool(True)),
                    kernel.Bool(False),
                    kernel.Bool(True),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_not(
    expr: sugar.Var,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.And, kernel.Expression]](
        [
            (
                sugar.And([]),
                kernel.Bool(True),
            ),
            (
                sugar.And([sugar.Bool(True)]),
                kernel.If(
                    condition=kernel.Bool(value=True),
                    consequent=kernel.Bool(value=True),
                    alternative=kernel.Bool(value=True),
                ),
            ),
            (
                sugar.And([sugar.Bool(True), sugar.Bool(False)]),
                kernel.If(
                    condition=kernel.Bool(value=True),
                    consequent=kernel.If(
                        condition=kernel.Bool(value=False),
                        consequent=kernel.Bool(value=True),
                        alternative=kernel.Bool(value=True),
                    ),
                    alternative=kernel.Bool(value=True),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_and(
    expr: sugar.And,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.Or, kernel.Expression]](
        [
            (
                sugar.Or([]),
                kernel.Bool(False),
            ),
            (
                sugar.Or([sugar.Bool(True)]),
                kernel.If(
                    condition=kernel.Bool(value=True),
                    consequent=kernel.Bool(value=True),
                    alternative=kernel.Bool(value=False),
                ),
            ),
            (
                sugar.Or([sugar.Bool(True), sugar.Bool(False)]),
                kernel.If(
                    condition=kernel.Bool(value=True),
                    consequent=kernel.Bool(value=True),
                    alternative=kernel.If(
                        condition=kernel.Bool(value=False),
                        consequent=kernel.Bool(value=True),
                        alternative=kernel.Bool(value=False),
                    ),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_or(
    expr: sugar.And,
    expected: kernel.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.If, kernel.Expression]](
        [
            (
                sugar.If(sugar.Bool(True), sugar.Var("x"), sugar.Var("y")),
                kernel.If(kernel.Bool(True), kernel.Var("x"), kernel.Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_if(
    expr: sugar.If,
    expected: kernel.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.LessThan, kernel.Expression]](
        [
            (
                sugar.LessThan([sugar.Int(1), sugar.Int(2)]),
                kernel.Binary("<", kernel.Int(1), kernel.Int(2)),
            ),
            (
                sugar.LessThan([sugar.Int(1), sugar.Int(2), sugar.Int(3)]),
                kernel.If(
                    condition=kernel.Binary(operator="<", x=kernel.Int(value=1), y=kernel.Int(value=2)),
                    consequent=kernel.If(
                        condition=kernel.Binary(operator="<", x=kernel.Int(value=2), y=kernel.Int(value=3)),
                        consequent=kernel.Bool(value=True),
                        alternative=kernel.Bool(value=True),
                    ),
                    alternative=kernel.Bool(value=True),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_less_than(
    expr: sugar.LessThan,
    expected: kernel.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.LessThanOrEqualTo, kernel.Expression]](
        [
            (
                sugar.LessThanOrEqualTo([sugar.Int(1), sugar.Int(2)]),
                kernel.Binary(">=", kernel.Int(2), kernel.Int(1)),
            ),
            (
                sugar.LessThanOrEqualTo([sugar.Int(1), sugar.Int(2), sugar.Int(3)]),
                kernel.If(
                    condition=kernel.Binary(operator=">=", x=kernel.Int(value=2), y=kernel.Int(value=1)),
                    consequent=kernel.If(
                        condition=kernel.Binary(operator=">=", x=kernel.Int(value=3), y=kernel.Int(value=2)),
                        consequent=kernel.Bool(value=True),
                        alternative=kernel.Bool(value=True),
                    ),
                    alternative=kernel.Bool(value=True),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_less_than_or_equal_to(
    expr: sugar.LessThan,
    expected: kernel.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.EqualTo, kernel.Expression]](
        [
            (
                sugar.EqualTo([sugar.Int(1), sugar.Int(2)]),
                kernel.Binary("==", kernel.Int(1), kernel.Int(2)),
            ),
            (
                sugar.EqualTo([sugar.Int(1), sugar.Int(2), sugar.Int(3)]),
                kernel.If(
                    condition=kernel.Binary(operator="==", x=kernel.Int(value=1), y=kernel.Int(value=2)),
                    consequent=kernel.If(
                        condition=kernel.Binary(operator="==", x=kernel.Int(value=2), y=kernel.Int(value=3)),
                        consequent=kernel.Bool(value=True),
                        alternative=kernel.Bool(value=True),
                    ),
                    alternative=kernel.Bool(value=True),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_equal_to(
    expr: sugar.LessThan,
    expected: kernel.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.GreaterThan, kernel.Expression]](
        [
            (
                sugar.GreaterThan([sugar.Int(1), sugar.Int(2)]),
                kernel.Binary("<", kernel.Int(2), kernel.Int(1)),
            ),
            (
                sugar.GreaterThan([sugar.Int(1), sugar.Int(2), sugar.Int(3)]),
                kernel.If(
                    condition=kernel.Binary(operator="<", x=kernel.Int(value=2), y=kernel.Int(value=1)),
                    consequent=kernel.If(
                        condition=kernel.Binary(operator="<", x=kernel.Int(value=3), y=kernel.Int(value=2)),
                        consequent=kernel.Bool(value=True),
                        alternative=kernel.Bool(value=True),
                    ),
                    alternative=kernel.Bool(value=True),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_greater_than(
    expr: sugar.GreaterThan,
    expected: kernel.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sugar.GreaterThanOrEqualTo, kernel.Expression]](
        [
            (
                sugar.GreaterThanOrEqualTo([sugar.Int(1), sugar.Int(2)]),
                kernel.Binary(">=", kernel.Int(1), kernel.Int(2)),
            ),
            (
                sugar.GreaterThanOrEqualTo([sugar.Int(1), sugar.Int(2), sugar.Int(3)]),
                kernel.If(
                    condition=kernel.Binary(operator=">=", x=kernel.Int(value=1), y=kernel.Int(value=2)),
                    consequent=kernel.If(
                        condition=kernel.Binary(operator=">=", x=kernel.Int(value=2), y=kernel.Int(value=3)),
                        consequent=kernel.Bool(value=True),
                        alternative=kernel.Bool(value=True),
                    ),
                    alternative=kernel.Bool(value=True),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_greater_than_or_equal_to(
    expr: sugar.GreaterThanOrEqualTo,
    expected: kernel.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected
