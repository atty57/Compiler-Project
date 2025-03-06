from collections.abc import Iterator, Sequence
from itertools import count
import pytest
from maltose import (
    Program,
    Atom,
    Int,
    Var,
    Bool,
    Unit,
    Expression,
    Add,
    Subtract,
    Multiply,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Tuple,
    Get,
    Set,
    Lambda,
    Copy,
    Statement,
    Let,
    If,
    Apply,
    Halt,
)
from eval import Value, Closure, Location, Environment, Store, eval, eval_statement, eval_expression, eval_atom


class SequentialLocationGenerator:
    def __init__(self):
        self.count = count(0)

    def __call__(self) -> Location:
        return Location(next(self.count))


@pytest.mark.parametrize(
    "program, arguments, expected",
    list[tuple[Program, Sequence[Int], tuple[Value, Store]]](
        [
            (
                Program([], Halt(Int(0))),
                [],
                (Int(0), {}),
            ),
            (
                Program(["x"], Halt(Var("x"))),
                [Int(0)],
                (Int(0), {}),
            ),
        ]
    ),
)
def test_eval(
    program: Program,
    arguments: Sequence[Int],
    expected: Value,
) -> None:
    assert eval(program, arguments) == expected


@pytest.mark.parametrize(
    "stmt, env, store, locations, expected",
    list[tuple[Statement, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Let("x", Copy(Int(1)), Halt(Var("x"))),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Int(1), {}),
            ),
        ]
    ),
)
def test_eval_statement_let(
    stmt: Statement,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_statement(stmt, env, store, locations) == expected


@pytest.mark.parametrize(
    "stmt, env, store, locations, expected",
    list[tuple[Statement, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                If(Bool(True), Halt(Int(10)), Halt(Int(20))),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Int(10), {}),
            ),
            (
                If(Bool(False), Halt(Int(10)), Halt(Int(20))),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Int(20), {}),
            ),
        ]
    ),
)
def test_eval_statement_if(
    stmt: Statement,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_statement(stmt, env, store, locations) == expected


@pytest.mark.parametrize(
    "stmt, env, store, locations, expected",
    list[tuple[Statement, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Apply(Var("id"), [Int(0)]),
                {"id": Closure(Lambda(["x"], Halt(Var("x"))), {})},
                {},
                map(lambda i: Location(i), count(0)),
                (Int(0), {}),
            ),
        ]
    ),
)
def test_eval_statement_apply(
    stmt: Statement,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_statement(stmt, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Int(2), {}),
            ),
        ]
    ),
)
def test_eval_expr_add(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Int(0), {}),
            ),
        ]
    ),
)
def test_eval_expr_subtract(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Multiply(Int(1), Int(2)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Int(2), {}),
            ),
        ]
    ),
)
def test_eval_multiply(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                LessThan(Int(1), Int(2)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Bool(True), {}),
            ),
        ]
    ),
)
def test_eval_expr_less_than(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                EqualTo(Int(1), Int(2)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Bool(False), {}),
            ),
            (
                EqualTo(Bool(True), Bool(True)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Bool(True), {}),
            ),
        ]
    ),
)
def test_eval_expr_equal_to(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                GreaterThanOrEqualTo(Int(2), Int(1)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Bool(True), {}),
            ),
        ]
    ),
)
def test_eval_expr_greater_than_or_equal_to(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Tuple([]),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Location(0), {Location(0): []}),
            ),
        ]
    ),
)
def test_eval_expr_tuple(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Get(Var("t"), Int(0)),
                {"t": Location(0)},
                {Location(0): [Int(0)]},
                map(lambda i: Location(i), count(0)),
                (Int(0), {Location(0): [Int(0)]}),
            ),
        ]
    ),
)
def test_eval_expr_get(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Set(Var("t"), Int(0), Int(1)),
                {"t": Location(0)},
                {Location(0): [Int(0)]},
                map(lambda i: Location(i), count(0)),
                (Unit(), {Location(0): [Int(1)]}),
            ),
        ]
    ),
)
def test_eval_expr_set(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], tuple[Value, Store]]](
        [
            (
                Lambda[Statement]([], Halt(Unit())),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                (Closure(Lambda([], Halt(Unit())), {}), {}),
            ),
        ]
    ),
)
def test_eval_expr_lambda(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations) == expected


@pytest.mark.parametrize(
    "atom, env, expected",
    list[tuple[Atom, Environment, Value]](
        [
            (
                Int(0),
                {},
                Int(0),
            ),
        ]
    ),
)
def test_eval_atom_int(
    atom: Int,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_atom(atom, env) == expected


@pytest.mark.parametrize(
    "atom, env, expected",
    list[tuple[Atom, Environment, Value]](
        [
            (
                Var("x"),
                {"x": Int(0)},
                Int(0),
            ),
        ]
    ),
)
def test_eval_atom_var(
    atom: Atom,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_atom(atom, env) == expected


@pytest.mark.parametrize(
    "atom, env, expected",
    list[tuple[Atom, Environment, Value]](
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
def test_eval_atom_bool(
    atom: Atom,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_atom(atom, env) == expected


@pytest.mark.parametrize(
    "atom, env, expected",
    list[tuple[Atom, Environment, Value]](
        [
            (
                Unit(),
                {},
                Unit(),
            ),
        ]
    ),
)
def test_eval_atom_unit(
    atom: Atom,
    env: Environment,
    expected: Value,
) -> None:
    assert eval_atom(atom, env) == expected
