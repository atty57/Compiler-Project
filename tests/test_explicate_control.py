from collections.abc import Callable, Sequence
import pytest
import glucose
from glucose import (
    Int,
    Add,
    Subtract,
    Multiply,
    Div,
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
import maltose
from maltose import (
    Copy,
    Halt,
)
from util import SequentialNameGenerator
from explicate_control import explicate_control, explicate_control_expression, explicate_control_expressions


@pytest.mark.parametrize(
    "program, fresh, expected",
    list[tuple[glucose.Program, Callable[[str], str], maltose.Program]](
        [
            (
                glucose.Program([], Int(0)),
                SequentialNameGenerator(),
                maltose.Program([], Halt(Int(0))),
            ),
        ]
    ),
)
def test_explicate_control(
    program: glucose.Program,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control(program, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Int(0),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Halt(Int(0)),
            ),
        ]
    ),
)
def test_explicate_control_expression_int(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Add(Int(0), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Add(Int(0), Int(0)), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_add(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Subtract(Int(0), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Subtract(Int(0), Int(0)), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_subtract(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Multiply(Int(0), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Multiply(Int(0), Int(0)), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_multiply(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Div(Int(0), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Copy(Div(Int(0), Int(0))), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_div(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Let("x", Unit(), Var("y")),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("x", Copy(Unit()), Halt(Var("y"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_let(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Var("x"),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Halt(Var("x")),
            ),
        ]
    ),
)
def test_explicate_control_expression_var(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Bool(True),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Halt(Bool(True)),
            ),
        ]
    ),
)
def test_explicate_control_expression_bool(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                If(Bool(True), Int(1), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let(
                    "_j0",
                    Lambda(["_t0"], Halt(Var("_t0"))),
                    If(Bool(True), Apply(Var("_j0"), [Int(1)]), Apply(Var("_j0"), [Int(0)])),
                ),
            ),
        ]
    ),
)
def test_explicate_control_expression_if(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                LessThan(Int(0), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", LessThan(Int(0), Int(0)), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_less_than(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                EqualTo(Int(0), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", EqualTo(Int(0), Int(0)), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_equal_to(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                GreaterThanOrEqualTo(Int(0), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", GreaterThanOrEqualTo(Int(0), Int(0)), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_greater_than_or_equal_to(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Unit(),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Halt(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_expression_unit(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Tuple([]),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Tuple([]), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_tuple(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Get(Var("x"), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Get(Var("x"), Int(0)), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_get(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Set(Var("x"), Int(0), Var("y")),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Set(Var("x"), Int(0), Var("y")), Halt(Var("_t0"))),
            ),
        ]
    ),
)
def test_explicate_control_expression_set(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Do(Var("y"), Var("x")),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Halt(Var("x")),
            ),
            (
                Do(Set(Var("x"), Int(0), Var("y")), Int(0)),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let("_t0", Set(Var("x"), Int(0), Var("y")), Halt(Int(0))),
            ),
        ]
    ),
)
def test_explicate_control_expression_do(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Lambda([], Unit()),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let(
                    "_t0",
                    Lambda(["_k0"], Apply(Var("_k0"), [Unit()])),
                    Halt(Var("_t0")),
                ),
            ),
            (
                Lambda(["x"], Var("x")),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let(
                    "_t0",
                    Lambda(["x", "_k0"], Apply(Var("_k0"), [Var("x")])),
                    Halt(Var("_t0")),
                ),
            ),
        ]
    ),
)
def test_explicate_control_expression_lambda(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "expr, k, fresh, expected",
    list[
        tuple[
            glucose.Expression,
            Callable[[maltose.Atom], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                Apply(Var("x"), []),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let(
                    "_k0",
                    Lambda(["_t0"], Halt(Var("_t0"))),
                    Apply(Var("x"), [Var("_k0")]),
                ),
            ),
            (
                Apply(Var("x"), [Int(0)]),
                lambda v: Halt(v),
                SequentialNameGenerator(),
                Let(
                    "_k0",
                    Lambda(["_t0"], Halt(Var("_t0"))),
                    Apply(Var("x"), [Int(0), Var("_k0")]),
                ),
            ),
        ]
    ),
)
def test_explicate_control_expression_apply(
    expr: glucose.Expression,
    k: Callable[[maltose.Atom], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expression(expr, k, fresh) == expected


@pytest.mark.parametrize(
    "exprs, k, fresh, expected",
    list[
        tuple[
            Sequence[glucose.Expression],
            Callable[[Sequence[maltose.Atom]], maltose.Statement],
            Callable[[str], str],
            maltose.Statement,
        ]
    ](
        [
            (
                [],
                lambda vs: Let("t", Tuple(vs), Halt(Var("t"))),
                SequentialNameGenerator(),
                Let("t", Tuple([]), Halt(Var("t"))),
            ),
            (
                [Int(0), Int(0)],
                lambda vs: Let("t", Tuple(vs), Halt(Var("t"))),
                SequentialNameGenerator(),
                Let("t", Tuple([Int(0), Int(0)]), Halt(Var("t"))),
            ),
        ]
    ),
)
def test_explicate_control_expressions(
    exprs: Sequence[glucose.Expression],
    k: Callable[[Sequence[maltose.Atom]], maltose.Statement],
    fresh: Callable[[str], str],
    expected: maltose.Statement,
) -> None:
    assert explicate_control_expressions(exprs, k, fresh) == expected
