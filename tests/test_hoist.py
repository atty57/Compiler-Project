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


@pytest.mark.xfail()
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


@pytest.mark.xfail()
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
def test_hoist_statement_let_lambda(
    stmt: maltose.Statement,
    fresh: Callable[[str], str],
    expected: lactose.Statement,
) -> None:
    assert hoist_statement(stmt, fresh) == expected


@pytest.mark.xfail()
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


@pytest.mark.xfail()
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


@pytest.mark.xfail()
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


@pytest.mark.xfail()
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
