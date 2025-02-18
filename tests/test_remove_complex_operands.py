from collections.abc import Callable, Sequence
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
    Unit,
    Tuple,
    Get,
    Set,
    Do,
    While,
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
    "program, fresh, expected",
    list[tuple[kernel.Program, Callable[[str], str], monadic.Program]](
        [
            (
                kernel.Program([], Int(0)),
                SequentialNameGenerator(),
                monadic.Program([], Int(0)),
            ),
        ]
    ),
)
def test_remove_complex_operands(
    program: kernel.Program,
    fresh: Callable[[str], str],
    expected: monadic.Program,
) -> None:
    assert remove_complex_operands(program, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Int(0),
                SequentialNameGenerator(),
                Int(0),
            ),
        ]
    ),
)
def test_rco_expr_int(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Add(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Add(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_add(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Subtract(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Subtract(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_subtract(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Multiply(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Multiply(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_multiply(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Let("x", Int(0), Var("x")),
                SequentialNameGenerator(),
                Let("x", Int(0), Var("x")),
            ),
        ]
    ),
)
def test_rco_expr_let(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Bool(True),
                SequentialNameGenerator(),
                Bool(True),
            ),
        ]
    ),
)
def test_rco_expr_bool(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                SequentialNameGenerator(),
                If(Var("c"), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_if(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                LessThan(Var("x"), Var("y")),
                SequentialNameGenerator(),
                LessThan(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_less_than(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                EqualTo(Var("x"), Var("y")),
                SequentialNameGenerator(),
                EqualTo(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_equal_to(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                GreaterThanOrEqualTo(Var("x"), Var("y")),
                SequentialNameGenerator(),
                GreaterThanOrEqualTo(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_greater_than_or_equal_to(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Unit(),
                SequentialNameGenerator(),
                Unit(),
            ),
        ]
    ),
)
def test_rco_expr_unit(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Tuple([Unit()]),
                SequentialNameGenerator(),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_rco_expr_cell(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Get(Var("x"), 0),
                SequentialNameGenerator(),
                Get(Var("x"), 0),
            ),
        ]
    ),
)
def test_rco_expr_get(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Set(Var("x"), 0, Var("y")),
                SequentialNameGenerator(),
                Set(Var("x"), 0, Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_set(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                Do(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Do(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_seq(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], monadic.Expression]](
        [
            (
                While(Var("x"), Var("y")),
                SequentialNameGenerator(),
                While(Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_rco_expr_while(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert rco_expr(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Int(0),
                SequentialNameGenerator(),
                (Int(0), []),
            ),
        ]
    ),
)
def test_rco_atom_int(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Add(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", Add(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_add(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Subtract(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", Subtract(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_subtract(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Multiply(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", Multiply(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_multiply(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Let("x", Int(0), Var("y")),
                SequentialNameGenerator(),
                (Var("y"), [("x", Int(0))]),
            ),
        ]
    ),
)
def test_rco_atom_let(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Var("x"),
                SequentialNameGenerator(),
                (Var("x"), []),
            ),
        ]
    ),
)
def test_rco_atom_var(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Bool(True),
                SequentialNameGenerator(),
                (Bool(True), []),
            ),
        ]
    ),
)
def test_rco_atom_bool(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", If(Var("c"), Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_if(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                LessThan(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", LessThan(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_less_then(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                EqualTo(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", EqualTo(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_equal_to(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                GreaterThanOrEqualTo(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", GreaterThanOrEqualTo(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_greater_than_or_equal_to(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Unit(),
                SequentialNameGenerator(),
                (Unit(), []),
            ),
        ]
    ),
)
def test_rco_atom_unit(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Tuple([Var("x")]),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", Tuple([Var("x")]))]),
            ),
        ]
    ),
)
def test_rco_atom_cell(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Get(Var("x"), 0),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", Get(Var("x"), 0))]),
            ),
        ]
    ),
)
def test_rco_atom_get(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Set(Var("x"), 0, Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", Set(Var("x"), 0, Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_set(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                Do(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", Do(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_seq(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
    assert rco_atom(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[kernel.Expression, Callable[[str], str], tuple[Atom, Sequence[Binding]]]](
        [
            (
                While(Var("x"), Var("y")),
                SequentialNameGenerator(),
                (Var("_t0"), [("_t0", While(Var("x"), Var("y")))]),
            ),
        ]
    ),
)
def test_rco_atom_while(
    expr: kernel.Expression,
    fresh: Callable[[str], str],
    expected: tuple[monadic.Expression, Sequence[Binding]],
) -> None:
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
