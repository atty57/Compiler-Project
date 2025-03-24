from collections.abc import Callable
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
    Apply,
    If,
    Halt,
)
from util import SequentialNameGenerator
from close_lambdas import (
    close,
    close_statement,
    free_variables_statement,
    free_variables_expression,
    free_variables_atom,
)
from typing import cast


def test_close_statement_unknown():
    fresh = SequentialNameGenerator()

    class Dummy:
        pass

    with pytest.raises(NotImplementedError):
        close_statement(Dummy(), fresh)


def test_close_program_no_lambda():
    fresh = SequentialNameGenerator()
    prog = Program(parameters=[], body=Halt(Int(0)))
    closed = close(prog, fresh)
    # Without any lambda, the program should remain essentially unchanged.
    assert closed.body == prog.body


def test_close_statement_let_lambda_basic():
    fresh = SequentialNameGenerator()
    stmt = Let("x", cast(Expression, Lambda([], cast(Statement, Halt(Int(0))))), cast(Statement, Halt(Int(0))))
    closed = close_statement(stmt, fresh)
    assert isinstance(closed, Let)


def test_close_statement_apply_no_args():
    fresh = SequentialNameGenerator()
    stmt: Statement = Apply(cast(Atom, Var("x")), [])
    closed = close_statement(stmt, fresh)
    closed = close_statement(stmt, fresh)
    # The no-arguments branch should wrap func into a Let
    assert isinstance(closed, Let)


def test_free_variables_atom_fn():
    assert free_variables_atom(Int(5)) == set()
    assert free_variables_atom(Var("x")) == {"x"}
    assert free_variables_expression(Var("")) == {""}


def test_free_variables_expression_fn():
    expr = Add(cast(Atom, Var("x")), cast(Atom, Int(3)))
    assert free_variables_expression(expr) == {"x"}


def test_free_variables_statement_fn():
    stmt = Let("y", cast(Expression, Copy(Var("z"))), cast(Statement, Halt(Var("x"))))
    assert free_variables_statement(stmt) == {"x", "z"}


def test_close_statement_apply_with_args():
    from maltose import Apply, Var, Let, Lambda, Halt, Int
    from close_lambdas import close_statement
    from util import SequentialNameGenerator

    fresh = SequentialNameGenerator()
    stmt = Apply(Var("x"), [Var("y")])
    closed = close_statement(stmt, fresh)
    expected = Let("_k0", Lambda(["_t0"], Halt(Var("_t0"))), Apply(Var("x"), [Var("y"), Var("_k0")]))
    assert closed == expected


@pytest.mark.parametrize(
    "program, fresh, expected",
    list[tuple[Program, Callable[[str], str], Program]](
        [
            (
                Program([], Halt(Int(0))),
                SequentialNameGenerator(),
                Program([], Halt(Int(0))),
            ),
        ]
    ),
)
def test_close(
    program: Program,
    fresh: Callable[[str], str],
    expected: Expression,
) -> None:
    assert close(program, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[tuple[Statement, Callable[[str], str], Statement]](
        [
            (
                Let("x", Lambda([], Halt(Int(0))), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("_t1", Lambda(["_t0"], Halt(Int(0))), Let("x", Tuple([Var("_t1")]), Halt(Int(0)))),
            ),
            (
                Let("x", Lambda(["x"], Halt(Var("x"))), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("_t1", Lambda(["_t0", "x"], Halt(Var("x"))), Let("x", Tuple([Var("_t1")]), Halt(Int(0)))),
            ),
            (
                Let("x", Lambda([], Halt(Var("x"))), Halt(Int(0))),
                SequentialNameGenerator(),
                Let(
                    "_t1",
                    Lambda(["_t0"], Let("x", Get(tuple=Var("_t0"), index=Int(1)), Halt(Var("x")))),
                    Let("x", Tuple([Var("_t1"), Var("x")]), Halt(Int(0))),
                ),
            ),
        ]
    ),
)
def test_close_statement_let_lambda(
    stmt: Statement,
    fresh: Callable[[str], str],
    expected: Statement,
) -> None:
    assert close_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[tuple[Statement, Callable[[str], str], Statement]](
        [
            (
                Let("x", Add(Int(0), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", Add(Int(0), Int(0)), Halt(Int(0))),
            ),
            (
                Let("x", Subtract(Int(0), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", Subtract(Int(0), Int(0)), Halt(Int(0))),
            ),
            (
                Let("x", Multiply(Int(0), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", Multiply(Int(0), Int(0)), Halt(Int(0))),
            ),
            (
                Let("x", LessThan(Int(0), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", LessThan(Int(0), Int(0)), Halt(Int(0))),
            ),
            (
                Let("x", EqualTo(Int(0), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", EqualTo(Int(0), Int(0)), Halt(Int(0))),
            ),
            (
                Let("x", GreaterThanOrEqualTo(Int(0), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", GreaterThanOrEqualTo(Int(0), Int(0)), Halt(Int(0))),
            ),
            (
                Let("x", Tuple([]), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", Tuple([]), Halt(Int(0))),
            ),
            (
                Let("x", Get(Var("x"), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", Get(Var("x"), Int(0)), Halt(Int(0))),
            ),
            (
                Let("x", Set(Var("x"), Int(0), Unit()), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", Set(Var("x"), Int(0), Unit()), Halt(Int(0))),
            ),
            (
                Let("x", Copy(Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                Let("x", Copy(Int(0)), Halt(Int(0))),
            ),
        ]
    ),
)
def test_close_statement_let_other(
    stmt: Statement,
    fresh: Callable[[str], str],
    expected: Statement,
) -> None:
    assert close_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[tuple[Statement, Callable[[str], str], Statement]](
        [
            (
                If(Var("x"), Halt(Int(0)), Halt(Int(1))),
                SequentialNameGenerator(),
                If(Var("x"), Halt(Int(0)), Halt(Int(1))),
            ),
        ]
    ),
)
def test_close_statement_if(
    stmt: Statement,
    fresh: Callable[[str], str],
    expected: Statement,
) -> None:
    assert close_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[tuple[Statement, Callable[[str], str], Statement]](
        [
            (
                Apply(Var("x"), []),
                SequentialNameGenerator(),
                Let("_t0", Get(Var("x"), Int(0)), Apply(Var("_t0"), [Var("x")])),
            ),
        ]
    ),
)
def test_close_statement_apply(
    stmt: Statement,
    fresh: Callable[[str], str],
    expected: Statement,
) -> None:
    assert close_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[tuple[Statement, Callable[[str], str], Statement]](
        [
            (
                Halt(Int(0)),
                SequentialNameGenerator(),
                Halt(Int(0)),
            ),
        ]
    ),
)
def test_close_statement_halt(
    stmt: Statement,
    fresh: Callable[[str], str],
    expected: Statement,
) -> None:
    assert close_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "atom, expected",
    list[tuple[Atom, set[str]]](
        [
            (
                Int(0),
                set(),
            ),
        ]
    ),
)
def test_free_variables_atom_int(
    atom: Atom,
    expected: set[str],
) -> None:
    assert free_variables_atom(atom) == expected


@pytest.mark.parametrize(
    "atom, expected",
    list[tuple[Atom, set[str]]](
        [
            (Var("x"), {"x"}),
        ]
    ),
)
def test_free_variables_atom_var(
    atom: Atom,
    expected: set[str],
) -> None:
    assert free_variables_atom(atom) == expected


@pytest.mark.parametrize(
    "atom, expected",
    list[tuple[Atom, set[str]]](
        [
            (
                Bool(True),
                set(),
            ),
        ]
    ),
)
def test_free_variables_atom_bool(
    atom: Atom,
    expected: set[str],
) -> None:
    assert free_variables_atom(atom) == expected


@pytest.mark.parametrize(
    "atom, expected",
    list[tuple[Atom, set[str]]](
        [
            (
                Unit(),
                set(),
            ),
        ]
    ),
)
def test_free_variables_atom_unit(
    atom: Atom,
    expected: set[str],
) -> None:
    assert free_variables_atom(atom) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Add(Var("x"), Var("y")),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_add(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Subtract(Var("x"), Var("y")),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_subtract(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Multiply(Var("x"), Var("y")),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_multiply(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                LessThan(Var("x"), Var("y")),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_less_than(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                EqualTo(Var("x"), Var("y")),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_equal_to(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                GreaterThanOrEqualTo(Var("x"), Var("y")),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_greater_than_or_equal_to(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Tuple([]),
                set(),
            ),
            (
                Tuple([Var("x"), Var("y")]),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_tuple(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Get(Var("x"), Var("y")),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_expression_get(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Set(Var("x"), Var("y"), Var("z")),
                {"x", "y", "z"},
            ),
        ]
    ),
)
def test_free_variables_expression_set(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Lambda[Statement]([], Halt(Var("x"))),
                {"x"},
            ),
            (
                Lambda[Statement](["x"], Halt(Var("x"))),
                set(),
            ),
        ]
    ),
)
def test_free_variables_expression_lambda(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "expr, expected",
    list[tuple[Expression, set[str]]](
        [
            (
                Copy(Unit()),
                set(),
            ),
        ]
    ),
)
def test_free_variables_expression_copy(
    expr: Expression,
    expected: set[str],
) -> None:
    assert free_variables_expression(expr) == expected


@pytest.mark.parametrize(
    "stmt, expected",
    list[tuple[Statement, set[str]]](
        [
            (
                Let("y", Copy(Var("z")), Halt(Var("x"))),
                {"x", "z"},
            ),
            (
                Let("x", Copy(Var("z")), Halt(Var("x"))),
                {"z"},
            ),
        ]
    ),
)
def test_free_variables_statement_let(
    stmt: Statement,
    expected: set[str],
) -> None:
    assert free_variables_statement(stmt) == expected


@pytest.mark.parametrize(
    "stmt, expected",
    list[tuple[Statement, set[str]]](
        [
            (
                If(Var("x"), Halt(Var("y")), Halt(Var("z"))),
                {"x", "y", "z"},
            ),
        ]
    ),
)
def test_free_variables_statement_if(
    stmt: Statement,
    expected: set[str],
) -> None:
    assert free_variables_statement(stmt) == expected


@pytest.mark.parametrize(
    "stmt, expected",
    list[tuple[Statement, set[str]]](
        [
            (
                Apply(Var("x"), [Var("y")]),
                {"x", "y"},
            ),
        ]
    ),
)
def test_free_variables_statement_apply(
    stmt: Statement,
    expected: set[str],
) -> None:
    assert free_variables_statement(stmt) == expected
