from collections.abc import Iterator, Sequence
from itertools import count
import pytest
from lactose import (
    Program,
    Lambda,
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
    Copy,
    Global,
    Statement,
    Let,
    If,
    Apply,
    Halt,
)
from eval_lactose import Value, Location, Environment, Store, Globals, eval, eval_statement, eval_expression, eval_atom


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
                Program([], Halt(Int(0)), {}),
                [],
                (Int(0), {}),
            ),
            (
                Program(["x"], Halt(Var("x")), {}),
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
    "stmt, env, store, locations, globals, expected",
    list[tuple[Statement, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Let("x", Copy(Int(1)), Halt(Var("x"))),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_statement(stmt, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "stmt, env, store, locations, globals, expected",
    list[tuple[Statement, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                If(Bool(True), Halt(Int(10)), Halt(Int(20))),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
                (Int(10), {}),
            ),
            (
                If(Bool(False), Halt(Int(10)), Halt(Int(20))),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_statement(stmt, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "stmt, env, store, locations, globals, expected",
    list[tuple[Statement, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Apply(Var("x"), [Int(0)]),
                {"x": Lambda[Statement](["x"], Halt(Var("x")))},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_statement(stmt, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Add(Int(1), Int(1)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Subtract(Int(1), Int(1)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Multiply(Int(1), Int(2)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                LessThan(Int(1), Int(2)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                EqualTo(Int(1), Int(2)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
                (Bool(False), {}),
            ),
            (
                EqualTo(Bool(True), Bool(True)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                GreaterThanOrEqualTo(Int(2), Int(1)),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Tuple([]),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Get(Var("t"), Int(0)),
                {"t": Location(0)},
                {Location(0): [Int(0)]},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Set(Var("t"), Int(0), Int(1)),
                {"t": Location(0)},
                {Location(0): [Int(0)]},
                map(lambda i: Location(i), count(0)),
                {},
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
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


@pytest.mark.parametrize(
    "expr, env, store, locations, globals, expected",
    list[tuple[Expression, Environment, Store, Iterator[Location], Globals, tuple[Value, Store]]](
        [
            (
                Global("f"),
                {},
                {},
                map(lambda i: Location(i), count(0)),
                {"f": Lambda([], Halt(Unit()))},
                (Lambda([], Halt[Atom](Unit())), {}),
            ),
        ]
    ),
)
def test_eval_expr_global(
    expr: Expression,
    env: Environment,
    store: Store,
    locations: Iterator[Location],
    globals: Globals,
    expected: Value,
) -> None:
    assert eval_expression(expr, env, store, locations, globals) == expected


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
