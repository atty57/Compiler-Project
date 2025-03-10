from collections.abc import Callable, Mapping
import pytest
from glucose import (
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
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    Lambda,
    Apply,
)
from uniqify import uniqify, uniqify_expression
from util import SequentialNameGenerator


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[Program, Callable[[str], str], Program]](
        [
            (
                Program([], Int(0)),
                SequentialNameGenerator(),
                Program([], Int(0)),
            ),
            (
                Program(["x"], Var("x")),
                SequentialNameGenerator(),
                Program(["_x0"], Var("_x0")),
            ),
        ]
    ),
)
def test_uniqify(
    expr: Program,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Int(0),
                {},
                SequentialNameGenerator(),
                Int(0),
            ),
        ]
    ),
)
def test_uniqify_expression_int(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                Add(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expression_add(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                Subtract(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expression_subtract(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Multiply(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                Multiply(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expression_multiply(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Let("x", Int(1), Var("x")),
                {},
                SequentialNameGenerator(),
                Let("_x0", Int(1), Var("_x0")),
            ),
            (
                Let("x", Int(1), Let("x", Int(2), Var("x"))),
                {},
                SequentialNameGenerator(),
                Let("_x0", Int(1), Let("_x1", Int(2), Var("_x1"))),
            ),
        ]
    ),
)
def test_uniqify_expression_let(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Var("x"),
                {"x": "y"},
                SequentialNameGenerator(),
                Var("y"),
            ),
        ]
    ),
)
def test_uniqify_expression_var(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Bool(True),
                {},
                SequentialNameGenerator(),
                Bool(True),
            ),
        ]
    ),
)
def test_uniqify_expression_bool(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                If(Bool(True), Int(2), Int(2)),
                {},
                SequentialNameGenerator(),
                If(Bool(True), Int(2), Int(2)),
            ),
        ]
    ),
)
def test_uniqify_expression_if(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                LessThan(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                LessThan(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expression_less_than(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                EqualTo(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                EqualTo(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expression_equal_to(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                GreaterThanOrEqualTo(Int(1), Int(1)),
                {},
                SequentialNameGenerator(),
                GreaterThanOrEqualTo(Int(1), Int(1)),
            ),
        ]
    ),
)
def test_uniqify_expression_greater_than_or_equal_to(
    expr: Expression,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Unit(),
                {},
                SequentialNameGenerator(),
                Unit(),
            ),
        ]
    ),
)
def test_uniqify_expression_unit(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Tuple([Unit()]),
                {},
                SequentialNameGenerator(),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_uniqify_expression_cell(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Get(Var("x"), Int(0)),
                {"x": "x"},
                SequentialNameGenerator(),
                Get(Var("x"), Int(0)),
            ),
        ]
    ),
)
def test_uniqify_expression_get(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Set(Var("x"), Int(0), Unit()),
                {"x": "x"},
                SequentialNameGenerator(),
                Set(Var("x"), Int(0), Unit()),
            ),
        ]
    ),
)
def test_uniqify_expression_set(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Do(Int(0), Unit()),
                {},
                SequentialNameGenerator(),
                Do(Int(0), Unit()),
            ),
        ]
    ),
)
def test_uniqify_expression_do(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Lambda([], Unit()),
                {},
                SequentialNameGenerator(),
                Lambda([], Unit()),
            ),
        ]
    ),
)
def test_uniqify_expression_lambda(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expression(expr, replacements, fresh) == expected


@pytest.mark.parametrize(
    "expr, replacements, fresh, expected",
    list[tuple[Expression, Mapping[str, str], Callable[[str], str], Expression]](
        [
            (
                Apply(Int(0), []),
                {},
                SequentialNameGenerator(),
                Apply(Int(0), []),
            ),
        ]
    ),
)
def test_uniqify_expression_apply(
    expr: Int,
    replacements: Mapping[str, str],
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert uniqify_expression(expr, replacements, fresh) == expected
