from collections.abc import Callable
import pytest
import maltose
import lactose
from maltose import (
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
from lactose import Block, Assign, Return, Jump
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
    list[tuple[maltose.Program, Callable[[str], str], lactose.Program]](
        [
            (
                maltose.Program([], Int(0)),
                SequentialNameGenerator(),
                lactose.Program([], Return(Int(0))),
            ),
        ]
    ),
)
def test_explicate_control(
    program: maltose.Program,
    fresh: Callable[[str], str],
    expected: lactose.Program,
) -> None:
    assert explicate_control(program, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
        [
            (
                Tuple([Unit()]),
                SequentialNameGenerator(),
                Return(Tuple([Unit()])),
            ),
        ]
    ),
)
def test_explicate_control_tail_cell(
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
        [
            (
                Get(Var("x"), 0),
                SequentialNameGenerator(),
                Return(Get(Var("x"), 0)),
            ),
        ]
    ),
)
def test_explicate_control_tail_get(
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
        [
            (
                Set(Var("x"), 0, Var("y")),
                SequentialNameGenerator(),
                Do(Set(Var("x"), 0, Var("y")), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_tail_set(
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[maltose.Expression, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_tail(expr, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                "x",
                Tuple([Unit()]),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Tuple([Unit()])), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_cell(
    dest: str,
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                "x",
                Get(Var("y"), 0),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Assign("x", Get(Var("y"), 0)), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_assign_get(
    dest: str,
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                "x",
                Set(Var("x"), 0, Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Set(Var("x"), 0, Var("y")), Do(Assign("x", Unit()), Return(Unit()))),
            ),
        ]
    ),
)
def test_explicate_control_assign_set(
    dest: str,
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "dest, expr, next, fresh, expected",
    list[tuple[str, maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_assign(dest, expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
        [
            (
                Tuple([Unit()]),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_cell(
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                Get(Var("x"), 0),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
                Do(
                    Assign("_t0", Get(Var("x"), 0)),
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
        [
            (
                Set(Var("x"), 0, Var("y")),
                Return(Var("then")),
                Return(Var("otherwise")),
                SequentialNameGenerator(),
            ),
        ]
    ),
)
def test_explicate_control_predicate_set(
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
    expected: lactose.Tail,
) -> None:
    assert explicate_control_predicate(expr, then, otherwise, fresh) == expected


@pytest.mark.parametrize(
    "expr, then, otherwise, fresh",
    list[tuple[maltose.Expression, lactose.Tail, lactose.Tail, Callable[[str], str]]](
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
    expr: maltose.Expression,
    then: lactose.Tail,
    otherwise: lactose.Tail,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(Exception):
        explicate_control_predicate(expr, then, otherwise, fresh)


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                If(Var("c"), Var("y"), Var("z")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do[lactose.Statement, lactose.Tail](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                Tuple([Unit()]),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_cell(
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                Get(Var("y"), 0),
                Return(Unit()),
                SequentialNameGenerator(),
                Return(Unit()),
            ),
        ]
    ),
)
def test_explicate_control_effect_get(
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
        [
            (
                Set(Var("x"), 0, Var("y")),
                Return(Unit()),
                SequentialNameGenerator(),
                Do(Set(Var("x"), 0, Var("y")), Return(Unit())),
            ),
        ]
    ),
)
def test_explicate_control_effect_set(
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected


@pytest.mark.parametrize(
    "expr, next, fresh, expected",
    list[tuple[maltose.Expression, lactose.Tail, Callable[[str], str], lactose.Tail]](
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
    expr: maltose.Expression,
    next: lactose.Tail,
    fresh: Callable[[str], str],
    expected: maltose.Expression,
) -> None:
    assert explicate_control_effect(expr, next, fresh) == expected
