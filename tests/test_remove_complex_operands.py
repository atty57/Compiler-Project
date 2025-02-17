from collections.abc import Sequence
import pytest
import kernel
import monadic
from kernel import (
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
from monadic import Atom
from remove_complex_operands import (
    Binding,
    remove_complex_operands,
    rco_expr,
    rco_atom,
    wrap,
)
from util import SequentialNameGenerator


@pytest.mark.parametrize(
    "program, expected",
    list[tuple[kernel.Program, monadic.Program]](
        [
            (
                kernel.Program([], Int(0)),
                monadic.Program([], Int(0)),
            ),
        ]
    ),
)
def test_remove_complex_operands(
    program: kernel.Program,
    expected: monadic.Program,
) -> None:
    fresh = SequentialNameGenerator()
    assert remove_complex_operands(program, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                Int(0),
                Int(0),
            ),
        ]
    ),
)
def test_rco_expr(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                Int(0),
                Int(0),
            ),
        ]
    ),
)
def test_rco_expr_int(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                Add(Var("x"), Var("y")),
                Add(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_add(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                Subtract(Var("x"), Var("y")),
                Subtract(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_subtract(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                Multiply(Var("x"), Var("y")),
                Multiply(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_multiply(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                Let("x", Int(0), Var("x")),
                Let("x", Int(0), Var("x")),
            ),
        ]
    ),
)
def test_rco_expr_let(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                Bool(True),
                Bool(True),
            ),
        ]
    ),
)
def test_rco_expr_bool(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                If(Var("c"), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_if(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                LessThan(Var("x"), Var("y")),
                LessThan(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_less_than(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                EqualTo(Var("x"), Var("y")),
                EqualTo(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_equal_to(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, monadic.Expression]](
        [
            (
                GreaterThanOrEqualTo(Var("x"), Var("y")),
                GreaterThanOrEqualTo(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_greater_than_or_equal_to(
    expr: kernel.Expression,
    expected: monadic.Expression,
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                Int(0),
                (Int(0), []),
            ),
        ]
    ),
)
def test_rco_atom_int(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                Add(Var("x"), Var("y")),
                (Var("_t0"), [("_t0", Add(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_add(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                Subtract(Var("x"), Var("y")),
                (Var("_t0"), [("_t0", Subtract(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_subtract(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                Multiply(Var("x"), Var("y")),
                (Var("_t0"), [("_t0", Multiply(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_multiply(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                Let("x", Int(0), Var("y")),
                (Var("y"), [("x", Int(0))]),
            ),
        ]
    ),
)
def test_rco_atom_let(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                Var("x"),
                (Var("x"), []),
            ),
        ]
    ),
)
def test_rco_atom_var(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                Bool(True),
                (Bool(True), []),
            ),
        ]
    ),
)
def test_rco_atom_bool(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                (Var("_t0"), [("_t0", If(Var("c"), Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_if(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                LessThan(Var("x"), Var("y")),
                (Var("_t0"), [("_t0", LessThan(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_less_then(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                EqualTo(Var("x"), Var("y")),
                (Var("_t0"), [("_t0", EqualTo(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_equal_to(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[kernel.Expression, tuple[Atom, Sequence[Binding]]]](
        [
            (
                GreaterThanOrEqualTo(Var("x"), Var("y")),
                (Var("_t0"), [("_t0", GreaterThanOrEqualTo(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_greater_than_or_equal_to(
    expr: kernel.Expression,
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    fresh = SequentialNameGenerator()
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "bindings, expr, expected",
    [
        (
            [],
            Int(0),
            Int(0),
        ),
        (
            [("x", Var("x"))],
            Int(0),
            Let("x", Var("x"), Int(0)),
        ),
        (
            [("x", Var("x")), ("y", Var("y"))],
            Int(0),
            Let("x", Var("x"), Let("y", Var("y"), Int(0))),
        ),
    ],
)
def test_wrap(
    bindings: Sequence[Binding],
    expr: monadic.Expression,
    expected: monadic.Expression,
) -> None:
    actual = wrap(bindings, expr)
    assert actual == expected
