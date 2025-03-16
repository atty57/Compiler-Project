from collections.abc import Callable, Mapping
import pytest
import maltose
from maltose import (
    Int,
    Var,
    Add,
    Lambda,
    Let,
    Apply,
    If,
    Halt,
)
import lactose
from lactose import Global
from util import SequentialNameGenerator
from hoist import (
    hoist,
    hoist_statement,
)


def test_hoist_statement_let_lambda():
    from typing import cast

    fresh = SequentialNameGenerator()
    stmt = cast(maltose.Statement, Let("x", Lambda([], Halt(Int(0))), Halt(Int(0))))
    closed, funcs = hoist_statement(stmt, fresh)
    # When the let binds a lambda, the branch should create a new function mapping.
    assert isinstance(closed, Let)
    assert isinstance(funcs, dict)
    assert len(funcs) == 1


def test_hoist_statement_if_simple():
    from typing import cast

    fresh = SequentialNameGenerator()
    stmt = cast(
        maltose.Statement,
        If(cast(maltose.Atom, Var("x")), cast(maltose.Statement, Halt(Int(0))), cast(maltose.Statement, Halt(Int(1)))),
    )
    _, funcs = hoist_statement(stmt, fresh)
    assert funcs == {}


def test_hoist_statement_apply_basic():
    from typing import cast

    fresh = SequentialNameGenerator()
    stmt = cast(maltose.Statement, Apply(Var("x"), []))
    closed, funcs = hoist_statement(stmt, fresh)
    assert funcs == {}
    assert isinstance(closed, Apply)


def test_hoist_statement_halt_basic():
    from typing import cast

    fresh = SequentialNameGenerator()
    stmt = cast(maltose.Statement, Halt(Int(1)))
    closed, funcs = hoist_statement(stmt, fresh)
    assert funcs == {}
    assert isinstance(closed, Halt)


def test_hoist_statement_unknown():
    fresh = SequentialNameGenerator()

    class Dummy:
        pass

    with pytest.raises(NotImplementedError):
        hoist_statement(Dummy(), fresh)


def test_hoist_program():
    fresh = SequentialNameGenerator()
    from maltose import Program

    prog = Program(parameters=[], body=Halt(Int(0)))
    hoisted = hoist(prog, fresh)
    assert hasattr(hoisted, "functions")
    assert isinstance(hoisted.functions, dict)


@pytest.mark.parametrize(
    "program, fresh, expected",
    list[tuple[maltose.Program, Callable[[str], str], lactose.Program]](
        [
            (
                maltose.Program([], Halt(Int(0))),
                SequentialNameGenerator(),
                lactose.Program([], Halt(Int(0)), {}),
            ),
        ]
    ),
)
def test_hoist(
    program: maltose.Program,
    fresh: Callable[[str], str],
    expected: lactose.Expression,
) -> None:
    assert hoist(program, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[
        tuple[
            maltose.Statement,
            Callable[[str], str],
            tuple[lactose.Statement, Mapping[str, lactose.Lambda[lactose.Statement]]],
        ]
    ](
        [
            (
                Let("x", Lambda([], Halt(Int(0))), Halt(Int(0))),
                SequentialNameGenerator(),
                (
                    Let("x", Global("_f0"), Halt(Int(0))),
                    {"_f0": Lambda([], Halt(Int(0)))},
                ),
            ),
        ]
    ),
)
def test_hoist_statement_let_lambda_parametrized(
    stmt: maltose.Statement,
    fresh: Callable[[str], str],
    expected: lactose.Statement,
) -> None:
    assert hoist_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[
        tuple[
            maltose.Statement,
            Callable[[str], str],
            tuple[lactose.Statement, Mapping[str, lactose.Lambda[lactose.Statement]]],
        ]
    ](
        [
            (
                Let("x", Add(Int(0), Int(0)), Halt(Int(0))),
                SequentialNameGenerator(),
                (
                    Let("x", Add(Int(0), Int(0)), Halt(Int(0))),
                    {},
                ),
            ),
        ]
    ),
)
def test_hoist_statement_let_other(
    stmt: maltose.Statement,
    fresh: Callable[[str], str],
    expected: lactose.Statement,
) -> None:
    assert hoist_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[
        tuple[
            maltose.Statement,
            Callable[[str], str],
            tuple[lactose.Statement, Mapping[str, lactose.Lambda[lactose.Statement]]],
        ]
    ](
        [
            (
                If(Var("x"), Halt(Int(0)), Halt(Int(1))),
                SequentialNameGenerator(),
                (
                    If(Var("x"), Halt(Int(0)), Halt(Int(1))),
                    {},
                ),
            ),
        ]
    ),
)
def test_hoist_statement_if(
    stmt: maltose.Statement,
    fresh: Callable[[str], str],
    expected: lactose.Statement,
) -> None:
    assert hoist_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[
        tuple[
            maltose.Statement,
            Callable[[str], str],
            tuple[lactose.Statement, Mapping[str, lactose.Lambda[lactose.Statement]]],
        ]
    ](
        [
            (
                Apply(Var("x"), []),
                SequentialNameGenerator(),
                (
                    Apply(Var("x"), []),
                    {},
                ),
            ),
        ]
    ),
)
def test_hoist_statement_apply(
    stmt: maltose.Statement,
    fresh: Callable[[str], str],
    expected: lactose.Statement,
) -> None:
    assert hoist_statement(stmt, fresh) == expected


@pytest.mark.parametrize(
    "stmt, fresh, expected",
    list[
        tuple[
            maltose.Statement,
            Callable[[str], str],
            tuple[lactose.Statement, Mapping[str, lactose.Lambda[lactose.Statement]]],
        ]
    ](
        [
            (
                Halt(Int(1)),
                SequentialNameGenerator(),
                (
                    Halt(Int(1)),
                    {},
                ),
            ),
        ]
    ),
)
def test_hoist_statement_halt(
    stmt: maltose.Statement,
    fresh: Callable[[str], str],
    expected: lactose.Statement,
) -> None:
    assert hoist_statement(stmt, fresh) == expected
