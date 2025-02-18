import pytest
import sucrose
from sucrose import (
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
    Unit,
    Cell,
    Get,
    Set,
    Do,
    Assign,
)
import glucose
from convert_assign import convert_assign, convert_assign_expr, mutable_variables


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[sucrose.Program, glucose.Program]](
        [
            (
                sucrose.Program([], Int(0)),
                glucose.Program([], Int(0)),
            ),
            (
                sucrose.Program(["x"], Int(0)),
                glucose.Program(["x"], Int(0)),
            ),
            (
                sucrose.Program(["x"], Assign("x", Int(0))),
                glucose.Program(["x"], Let("x", Cell(Var("x")), Set(Var("x"), Int(0)))),
            ),
        ]
    ),
)
def test_convert_assign(
    program: sucrose.Program,
    expected: glucose.Expression,
) -> None:
    print(convert_assign(program))
    assert convert_assign(program) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Int(0),
                set(),
                Int(0),
            ),
        ]
    ),
)
def test_convert_assign_expr_int(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Add(Int(0), Int(0)),
                set(),
                Add(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assign_expr_add(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Subtract(Int(0), Int(0)),
                set(),
                Subtract(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assign_expr_subtract(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Multiply(Int(0), Int(0)),
                set(),
                Multiply(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assign_expr_multiply(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Let("x", Int(0), Unit()),
                set(),
                Let("x", Int(0), Unit()),
            ),
        ]
    ),
)
def test_convert_assign_expr_let(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Var("x"),
                set(),
                Var("x"),
            ),
            (
                Var("x"),
                {"x"},
                Get(Var("x")),
            ),
        ]
    ),
)
def test_convert_assign_expr_var(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Bool(True),
                set(),
                Bool(True),
            ),
        ]
    ),
)
def test_convert_assign_expr_bool(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                set(),
                If(Var("c"), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_convert_assign_expr_if(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                LessThan(Int(0), Int(0)),
                set(),
                LessThan(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assign_expr_less_than(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                EqualTo(Int(0), Int(0)),
                set(),
                EqualTo(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assign_expr_equal_to(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                GreaterThanOrEqualTo(Int(0), Int(0)),
                set(),
                GreaterThanOrEqualTo(Int(0), Int(0)),
            ),
        ]
    ),
)
def test_convert_assign_expr_greater_than_or_equal_to(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Unit(),
                set(),
                Unit(),
            ),
        ]
    ),
)
def test_convert_assign_expr_unit(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Cell(Unit()),
                set(),
                Cell(Unit()),
            ),
        ]
    ),
)
def test_convert_assign_expr_cell(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Get(Var("x")),
                set(),
                Get(Var("x")),
            ),
        ]
    ),
)
def test_convert_assign_expr_get(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Set(Var("x"), Var("y")),
                set(),
                Set(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_convert_assign_expr_set(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Do(Var("x"), Var("y")),
                set(),
                Do(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_convert_assign_expr_do(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, vars, expected",
    list[tuple[sucrose.Expression, set[str], glucose.Expression]](
        [
            (
                Assign("x", Var("y")),
                set(),
                Set(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_convert_assign_expr_assign(
    expr: sucrose.Expression,
    vars: set[str],
    expected: glucose.Expression,
) -> None:
    assert convert_assign_expr(expr, vars) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[sucrose.Expression, set[str]]](
        [
            (Int(0), set()),
            (Add(Int(0), Int(0)), set()),
            (Subtract(Int(0), Int(0)), set()),
            (Multiply(Int(0), Int(0)), set()),
            (Let("x", Int(0), Unit()), set()),
            (Var("x"), set()),
            (Bool(True), set()),
            (If(Var("x"), Var("x"), Var("y")), set()),
            (LessThan(Int(0), Int(0)), set()),
            (EqualTo(Int(0), Int(0)), set()),
            (GreaterThanOrEqualTo(Int(0), Int(0)), set()),
            (Unit(), set()),
            (Cell(Unit()), set()),
            (Get(Var("x")), set()),
            (Set(Var("x"), Var("y")), set()),
            (Do(Var("x"), Var("y")), set()),
            (Assign("x", Var("y")), {"x"}),
        ]
    ),
)
def test_mutable_variables(
    expr: sucrose.Expression,
    expected: set[str],
) -> None:
    assert mutable_variables(expr) == expected
