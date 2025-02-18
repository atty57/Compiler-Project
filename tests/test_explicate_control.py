from collections.abc import Callable
import pytest
import monadic
import cps
from monadic import (
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
    Cell,
    Get,
    Set,
    Do,
    While,
)
from cps import Block, Assign, Return, Jump
from explicate_control import (
    explicate_control,
    explicate_control_tail,
    explicate_control_assign,
    explicate_control_predicate,
    explicate_control_effect,
)
from util import SequentialNameGenerator


@pytest.mark.parametrize(
    "program, fresh, expected",
    list[tuple[monadic.Program, Callable[[str], str], cps.Program]](
        [
            (
                monadic.Program([], Int(0)),
                SequentialNameGenerator(),
                cps.Program([], Return(Int(0))),
            ),
        ]
    ),
)
def test_explicate_control(
    program: monadic.Program,
    fresh: Callable[[str], str],
    expected: cps.Program,
) -> None:
    assert explicate_control(program, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Int(0),
                SequentialNameGenerator(),
                Return(Int(0)),
            ),
        ]
    ),
)
def test_explicate_control_tail_int(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Add(Int(0), Int(1)),
                SequentialNameGenerator(),
                Return(Add(Int(0), Int(1))),
            ),
        ]
    ),
)
def test_explicate_control_tail_add(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Subtract(Int(0), Int(1)),
                SequentialNameGenerator(),
                Return(Subtract(Int(0), Int(1))),
            ),
        ]
    ),
)
def test_explicate_control_tail_subtract(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Multiply(Int(0), Int(1)),
                SequentialNameGenerator(),
                Return(Multiply(Int(0), Int(1))),
            ),
        ]
    ),
)
def test_explicate_control_tail_multiply(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Let("x", Int(0), Int(1)),
                SequentialNameGenerator(),
                Do(Assign("x", Int(0)), Return(Int(1))),
            ),
        ]
    ),
)
def test_explicate_control_tail_let(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Var("x"),
                SequentialNameGenerator(),
                Return(Var("x")),
            ),
        ]
    ),
)
def test_explicate_control_tail_var(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Bool(True),
                SequentialNameGenerator(),
                Return(Bool(True)),
            ),
        ]
    ),
)
def test_explicate_control_tail_bool(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                SequentialNameGenerator(),
                Do(
                    Assign("_then0", Block(Return(Var("x")))),
                    Do(
                        Assign("_else0", Block(Return(Var("y")))),
                        If(Var("c"), Jump("_then0"), Jump("_else0")),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_tail_if(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                LessThan(Int(0), Int(1)),
                SequentialNameGenerator(),
                Return(LessThan(Int(0), Int(1))),
            ),
        ]
    ),
)
def test_explicate_control_tail_less_than(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                EqualTo(Int(0), Int(1)),
                SequentialNameGenerator(),
                Return(EqualTo(Int(0), Int(1))),
            ),
        ]
    ),
)
def test_explicate_control_tail_equal_to(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                GreaterThanOrEqualTo(Int(0), Int(1)),
                SequentialNameGenerator(),
                Return(GreaterThanOrEqualTo(Int(0), Int(1))),
            ),
        ]
    ),
)
def test_explicate_control_tail_greater_than_or_equal_to(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Unit(),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_tail_unit(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Cell(Unit()),
                SequentialNameGenerator(),
                Return(Cell(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_tail_cell(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Get(Var("x")),
                SequentialNameGenerator(),
                Return(Get(Var("x"))),
            ),
        ]
    ),
)
def test_explicate_control_tail_get(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Set(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Do(Set(Var("x"), Var("y")), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_tail_set(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                Do(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Return(Var("y")),
            ),
        ]
    ),
)
def test_explicate_control_tail_seq(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[monadic.Expression, Callable[[str], str], cps.Tail]](
        [
            (
                While(Var("x"), Var("y")),
                SequentialNameGenerator(),
                Do(
                    Assign(
                        "_loop0",
                        Block(
                            Do(
                                Assign("_then0", Block(Jump("_loop0"))),
                                Do(
                                    Assign("_else0", Block(Return(Unit()))),
                                    If(Var("x"), Jump("_then0"), Jump("_else0")),
                                ),
                            )
                        ),
                    ),
                    Jump("_loop0"),
                ),
            ),
        ]
    ),
)
def test_explicate_control_tail_while(
    expr: monadic.Expression,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Int(0),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Int(0)), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_int(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Add(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Add(Int(0), Int(0))), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_add(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Subtract(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Subtract(Int(0), Int(0))), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_subtract(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Multiply(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Multiply(Int(0), Int(0))), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_multiply(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Let("y", Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("y", Int(0)), Do(Assign("x", Int(0)), Return(Unit()))),
            ),
        ]
    ),
)
def test_explicate_control_assign_let(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Var("y"),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Var("y")), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_var(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Bool(True),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Bool(True)), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_bool(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                If(Var("c"), Var("y"), Var("z")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(
                    Assign("_then0", Block(Do(Assign("x", Var("y")), Return(Unit())))),
                    Do(
                        Assign("_else0", Block(Do(Assign("x", Var("z")), Return(Unit())))),
                        If(Var("c"), Jump("_then0"), Jump("_else0")),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_assign_if(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                LessThan(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", LessThan(Int(0), Int(0))), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_less_than(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                EqualTo(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", EqualTo(Int(0), Int(0))), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_equal_to(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                GreaterThanOrEqualTo(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", GreaterThanOrEqualTo(Int(0), Int(0))), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_greater_than_or_equal_to(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Unit(),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Unit()), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_unit(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Cell(Unit()),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Cell(Unit())), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_cell(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Get(Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Get(Var("y"))), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_get(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Set(Var("x"), Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Set(Var("x"), Var("y")), Do(Assign("x", Unit()), Return(Unit()))),
            ),
        ]
    ),
)
def test_explicate_control_assign_set(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                Do(Var("x"), Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Var("y")), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_seq(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                "x",
                While(Var("x"), Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(
                    Assign(
                        "_loop0",
                        Block(
                            Do(
                                Assign("_then0", Block(Jump("_loop0"))),
                                Do(
                                    Assign("_else0", Block(Do(Assign("x", Unit()), Return(Unit())))),
                                    If(Var("x"), Jump("_then0"), Jump("_else0")),
                                ),
                            )
                        ),
                    ),
                    Jump("_loop0"),
                ),
            ),
        ]
    ),
)
def test_explicate_control_assign_while(
    dest: str,
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                Int(0),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_int(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                Add(Int(0), Int(0)),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_add(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                Subtract(Int(0), Int(0)),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_subtract(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                Multiply(Int(0), Int(0)),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_multiply(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Let("x", Int(0), Var("y")),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("x", Int(0)),
                    Do(
                        Assign("_then0", Block(Return(Var("then")))),
                        Do(
                            Assign("_else0", Block(Return(Var("otherwise")))),
                            If(Var("y"), Jump("_then0"), Jump("_else0")),
                        ),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_let(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Var("x"),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("_then0", Block(Return(Var("then")))),
                    Do(
                        Assign("_else0", Block(Return(Var("otherwise")))),
                        If(Var("x"), Jump("_then0"), Jump("_else0")),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_var(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Bool(True),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Return(Var("then")),
            ),
            (
                Bool(False),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Return(Var("otherwise")),
            ),
        ]
    ),
)
def test_explicate_control_predicate_bool(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                If(Var("c"), Var("x"), Var("y")),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign(
                        "_then2",
                        Block(
                            Do(
                                Assign("_then0", Block(Return(Var("then")))),
                                Do(
                                    Assign("_else0", Block(Return(Var("otherwise")))),
                                    If(Var("x"), Jump("_then0"), Jump("_else0")),
                                ),
                            )
                        ),
                    ),
                    Do(
                        Assign(
                            "_else2",
                            Block(
                                Do(
                                    Assign("_then1", Block(Return(Var("then")))),
                                    Do(
                                        Assign("_else1", Block(Return(Var("otherwise")))),
                                        If(Var("y"), Jump("_then1"), Jump("_else1")),
                                    ),
                                )
                            ),
                        ),
                        If(Var("c"), Jump("_then2"), Jump("_else2")),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_if(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                LessThan(Int(0), Int(0)),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("_t0", LessThan(x=Int(0), y=Int(0))),
                    Do(
                        Assign("_then0", Block(Return(Var("then")))),
                        Do(
                            Assign("_else0", Block(Return(Var("otherwise")))),
                            If(Var("_t0"), Jump("_then0"), Jump("_else0")),
                        ),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_less_than(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                EqualTo(Int(0), Int(0)),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("_t0", EqualTo(x=Int(0), y=Int(0))),
                    Do(
                        Assign("_then0", Block(Return(Var("then")))),
                        Do(
                            Assign("_else0", Block(Return(Var("otherwise")))),
                            If(Var("_t0"), Jump("_then0"), Jump("_else0")),
                        ),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_equal_to(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                GreaterThanOrEqualTo(Int(0), Int(0)),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("_t0", GreaterThanOrEqualTo(x=Int(0), y=Int(0))),
                    Do(
                        Assign("_then0", Block(Return(Var("then")))),
                        Do(
                            Assign("_else0", Block(Return(Var("otherwise")))),
                            If(Var("_t0"), Jump("_then0"), Jump("_else0")),
                        ),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_greater_than_or_equal_to(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                Unit(),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_unit(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                Cell(Unit()),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_cell(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Get(Var("x")),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("_t0", Get(Var("x"))),
                    Do(
                        Assign("_then0", Block(Return(Var("then")))),
                        Do(
                            Assign("_else0", Block(Return(Var("otherwise")))),
                            If(Var("_t0"), Jump("_then0"), Jump("_else0")),
                        ),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_get(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                Set(Var("x"), Var("y")),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_set(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Do(Var("x"), Var("y")),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("_then0", Block(Return(Var("then")))),
                    Do(
                        Assign("_else0", Block(Return(Var("otherwise")))),
                        If(Var("y"), Jump("_then0"), Jump("_else0")),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_predicate_seq(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
    expected: cps.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[monadic.Expression, cps.Tail, cps.Tail, Callable[[str], str]]](
        [
            (
                While(Var("x"), Var("y")),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_while(
    expr: monadic.Expression,
    then: cps.Tail,
    otherwise: cps.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Int(0),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_int(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Add(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_add(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Subtract(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_subtract(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Multiply(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_multiply(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Let("y", Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("y", Int(0)), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_effect_let(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Var("y"),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_var(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Bool(True),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_bool(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                If(Var("c"), Var("y"), Var("z")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do[cps.Statement, cps.Tail](
                    Assign("_then0", Block(Return(Unit()))),
                    Do(
                        Assign("_else0", Block(Return(Unit()))),
                        If(Var("c"), Jump("_then0"), Jump("_else0")),
                    ),
                ),
            ),
        ]
    ),
)
def test_explicate_control_effect_if(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                LessThan(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_less_than(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                EqualTo(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_equal_to(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                GreaterThanOrEqualTo(Int(0), Int(0)),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_greater_than_or_equal_to(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Unit(),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_unit(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Cell(Unit()),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_cell(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Get(Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_get(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Set(Var("x"), Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Set(Var("x"), Var("y")), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_effect_set(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                Do(Var("x"), Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_seq(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[monadic.Expression, cps.Tail, Callable[[str], str], cps.Tail]](
        [
            (
                While(Var("x"), Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(
                    Assign(
                        "_loop0",
                        Block(
                            Do(
                                Assign("_then0", Block(Jump("_loop0"))),
                                Do(
                                    Assign("_else0", Block(Return(Unit()))),
                                    If(Var("x"), Jump("_then0"), Jump("_else0")),
                                ),
                            )
                        ),
                    ),
                    Jump("_loop0"),
                ),
            ),
        ]
    ),
)
def test_explicate_control_effect_while(
    expr: monadic.Expression,
    next: cps.Tail,
    fresh: Callable[[str], str],
    expected: monadic.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected
