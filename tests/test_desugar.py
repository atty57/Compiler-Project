import pytest
import fructose
from fructose import (
    Int,
    Let,
    Var,
    LetStar,
    Bool,
    Not,
    All,
    Any,
    If,
    Cond,
    Unit,
    Tuple,
    Get,
    Set,
    While,
    Assign,
    Cell,
    CellGet,
    CellSet,
    Vector,
    VectorLength,
    VectorGet,
    VectorSet,
)
import sucrose
from desugar import desugar, desugar_expr


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[fructose.Program, sucrose.Program]](
        [
            (
                fructose.Program([], Int(0)),
                sucrose.Program([], Int(0)),
            ),
        ]
    ),
)
def test_desugar(
    program: fructose.Program,
    expected: sucrose.Expression,
) -> None:
    assert desugar(program) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Int(0),
                Int(0),
            ),
        ]
    ),
)
def test_desugar_expr_int(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.Add([]),
                Int(0),
            ),
            (
                fructose.Add([Int(1)]),
                sucrose.Add(Int(1), Int(0)),
            ),
            (
                fructose.Add([Int(1), Int(1)]),
                sucrose.Add(Int(1), sucrose.Add(Int(1), Int(0))),
            ),
        ]
    ),
)
def test_desugar_expr_add(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.Subtract([Int(1)]),
                sucrose.Subtract(Int(0), Int(1)),
            ),
            (
                fructose.Subtract([Int(2), Int(1)]),
                sucrose.Subtract(Int(2), Int(1)),
            ),
            (
                fructose.Subtract([Int(3), Int(2), Int(1)]),
                sucrose.Subtract(Int(3), sucrose.Subtract(Int(2), Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_subtract(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.Multiply([]),
                Int(1),
            ),
            (
                fructose.Multiply([Int(1)]),
                sucrose.Multiply(Int(1), Int(1)),
            ),
            (
                fructose.Multiply([Int(2), Int(2)]),
                sucrose.Multiply(Int(2), sucrose.Multiply(Int(2), Int(1))),
            ),
        ]
    ),
)
def test_desugar_expr_multiply(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Let("x", Int(0), Var("x")),
                Let("x", Int(0), Var("x")),
            ),
        ]
    ),
)
def test_desugar_expr_let(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Var("x"),
                Var("x"),
            ),
        ]
    ),
)
def test_desugar_expr_var(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                LetStar([], Var("x")),
                Var("x"),
            ),
            (
                LetStar([("x", Int(0))], Var("x")),
                Let("x", Int(0), Var("x")),
            ),
            (
                LetStar([("x", Int(0)), ("y", Int(1))], Var("x")),
                Let(
                    "x",
                    Int(0),
                    Let("y", Int(1), Var("x")),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_letstar(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Bool(True),
                Bool(True),
            ),
        ]
    ),
)
def test_desugar_expr_bool(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Not(Var("x")),
                If(sucrose.EqualTo(Var("x"), Bool(True)), Bool(False), Bool(True)),
            ),
        ]
    ),
)
def test_desugar_expr_not(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                All([]),
                Bool(True),
            ),
            (
                All([Bool(True)]),
                If(Bool(True), Bool(True), Bool(False)),
            ),
            (
                All([Bool(True), Bool(False)]),
                If(Bool(True), If(Bool(False), Bool(True), Bool(False)), Bool(False)),
            ),
        ]
    ),
)
def test_desugar_expr_all(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Any([]),
                Bool(False),
            ),
            (
                Any([Bool(True)]),
                If(Bool(True), Bool(True), Bool(False)),
            ),
            (
                Any([Bool(True), Bool(False)]),
                If(Bool(True), Bool(True), If(Bool(False), Bool(True), Bool(False))),
            ),
        ]
    ),
)
def test_desugar_expr_any(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                If(Bool(True), Var("x"), Var("y")),
                If(Bool(True), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_if(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Cond([], Int(0)),
                Int(0),
            ),
            (
                Cond([(Bool(True), Int(1))], Int(0)),
                If(Bool(True), Int(1), Int(0)),
            ),
        ]
    ),
)
def test_desugar_expr_cond(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.LessThanOrEqualTo([]),
                Bool(True),
            ),
            (
                fructose.LessThanOrEqualTo([Int(0)]),
                Bool(True),
            ),
            (
                fructose.LessThanOrEqualTo([Int(1), Int(2)]),
                sucrose.GreaterThanOrEqualTo(Int(2), Int(1)),
            ),
            (
                fructose.LessThanOrEqualTo([Int(1), Int(2), Int(3)]),
                If(
                    sucrose.GreaterThanOrEqualTo(Int(2), Int(1)),
                    sucrose.GreaterThanOrEqualTo(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_less_than_or_equal_to(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    print(desugar_expr(expr))
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.LessThan([]),
                Bool(True),
            ),
            (
                fructose.LessThan([Int(0)]),
                Bool(True),
            ),
            (
                fructose.LessThan([Int(1), Int(2)]),
                sucrose.LessThan(Int(1), Int(2)),
            ),
            (
                fructose.LessThan([Int(1), Int(2), Int(3)]),
                If(
                    sucrose.LessThan(Int(1), Int(2)),
                    sucrose.LessThan(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_less_than(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.EqualTo([]),
                Bool(True),
            ),
            (
                fructose.EqualTo([Int(0)]),
                Bool(True),
            ),
            (
                fructose.EqualTo([Int(1), Int(2)]),
                sucrose.EqualTo(Int(1), Int(2)),
            ),
            (
                fructose.EqualTo([Int(1), Int(2), Int(3)]),
                If(
                    sucrose.EqualTo(Int(1), Int(2)),
                    sucrose.EqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_equal_to(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.GreaterThan([]),
                Bool(True),
            ),
            (
                fructose.GreaterThan([Int(0)]),
                Bool(True),
            ),
            (
                fructose.GreaterThan([Int(1), Int(2)]),
                sucrose.LessThan(Int(2), Int(1)),
            ),
            (
                fructose.GreaterThan([Int(1), Int(2), Int(3)]),
                If(
                    sucrose.LessThan(Int(2), Int(1)),
                    sucrose.LessThan(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_greater_than(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.GreaterThanOrEqualTo([]),
                Bool(True),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(0)]),
                Bool(True),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(1), Int(2)]),
                sucrose.GreaterThanOrEqualTo(Int(1), Int(2)),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(1), Int(2), Int(3)]),
                If(
                    sucrose.GreaterThanOrEqualTo(Int(1), Int(2)),
                    sucrose.GreaterThanOrEqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_desugar_expr_greater_than_or_equal_to(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Unit(),
                Unit(),
            ),
        ]
    ),
)
def test_desugar_expr_unit(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Tuple([Unit()]),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_desugar_expr_tuple(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Get(Var("x"), 0),
                Get(Var("x"), 0),
            ),
        ]
    ),
)
def test_desugar_expr_get(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Set(Var("x"), 0, Var("y")),
                Set(Var("x"), 0, Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_set(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                fructose.Do([]),
                Unit(),
            ),
            (
                fructose.Do([Int(0)]),
                Int(0),
            ),
            (
                fructose.Do([Unit(), Int(0)]),
                sucrose.Do(Unit(), Int(0)),
            ),
        ]
    ),
)
def test_desugar_expr_begin(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                While(Var("x"), Var("y")),
                While(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_while(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Assign("x", Var("y")),
                Assign("x", Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_assign(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Cell(Unit()),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_desugar_expr_cell(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                CellGet[fructose.Expression](Var("x")),
                Get(Var("x"), 0),
            ),
        ]
    ),
)
def test_desugar_expr_cell_get(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                CellSet(Var("x"), Var("y")),
                Set(Var("x"), 0, Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_cell_set(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                Vector([]),
                Tuple([Int(0)]),
            ),
            (
                Vector([Unit()]),
                Tuple([Int(1), Unit()]),
            ),
        ]
    ),
)
def test_desugar_expr_vector(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                VectorLength(Var("x")),
                Get(Var("x"), 0),
            ),
        ]
    ),
)
def test_desugar_expr_vector_length(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                VectorGet[fructose.Expression](Var("x"), 0),
                Get(Var("x"), 1),
            ),
        ]
    ),
)
def test_desugar_expr_vector_get(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[fructose.Expression, sucrose.Expression]](
        [
            (
                VectorSet(Var("x"), 0, Var("y")),
                Set(Var("x"), 1, Var("y")),
            ),
        ]
    ),
)
def test_desugar_expr_vector_set(
    expr: fructose.Expression,
    expected: sucrose.Expression,
) -> None:
    assert desugar_expr(expr) == expected
