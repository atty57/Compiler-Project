from collections.abc import Callable
import pytest
import fructose
from fructose import (
    Int,
    Var,
    LetStar,
    Bool,
    Not,
    And,
    Or,
    If,
    Cond,
    Unit,
    Begin,
    Cell,
    While,
    Lambda,
    Apply,
    Assign,
    Expression,
)
import sucrose
from sucrose import Tuple, Do
from util import SequentialNameGenerator
from simplify import simplify, simplify_expression


@pytest.mark.parametrize(
    "program, fresh, expected",
    list[tuple[fructose.Program, Callable[[str], str], sucrose.Program]](
        [
            (
                fructose.Program([], Int(0)),
                SequentialNameGenerator(),
                sucrose.Program([], Int(0)),
            ),
        ]
    ),
)
def test_desugar(
    program: fructose.Program,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify(program, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Int(0),
                SequentialNameGenerator(),
                Int(0),
            ),
        ]
    ),
)
def test_simplify_expression_int(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Add([]),
                SequentialNameGenerator(),
                Int(0),
            ),
            (
                fructose.Add([Int(1)]),
                SequentialNameGenerator(),
                Int(1),
            ),
            (
                fructose.Add([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                sucrose.Add(Int(1), sucrose.Add(Int(2), Int(3))),
            ),
        ]
    ),
)
def test_simplify_expression_add(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Subtract([Int(1)]),
                SequentialNameGenerator(),
                sucrose.Subtract(Int(0), Int(1)),
            ),
            (
                fructose.Subtract([Int(2), Int(1)]),
                SequentialNameGenerator(),
                sucrose.Subtract(Int(2), Int(1)),
            ),
            (
                fructose.Subtract([Int(3), Int(2), Int(1)]),
                SequentialNameGenerator(),
                sucrose.Subtract(Int(3), sucrose.Subtract(Int(2), Int(1))),
            ),
        ]
    ),
)
def test_simplify_expression_subtract(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Multiply([]),
                SequentialNameGenerator(),
                Int(1),
            ),
            (
                fructose.Multiply([Int(2)]),
                SequentialNameGenerator(),
                Int(2),
            ),
            (
                fructose.Multiply([Int(2), Int(2)]),
                SequentialNameGenerator(),
                sucrose.Multiply(Int(2), Int(2)),
            ),
            (
                fructose.Multiply([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                sucrose.Multiply(Int(1), sucrose.Multiply(Int(2), Int(3))),
            ),
        ]
    ),
)
def test_simplify_expression_multiply(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Div([]),
                SequentialNameGenerator(),
                Int(1),
            ),
            (
                fructose.Div([Int(2)]),
                SequentialNameGenerator(),
                Int(2),
            ),
            (
                fructose.Div([Int(2), Int(2)]),
                SequentialNameGenerator(),
                sucrose.Div(Int(2), Int(2)),
            ),
            (
                fructose.Div([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                sucrose.Div(Int(1), sucrose.Div(Int(2), Int(3))),
            ),
        ]
    ),
)
def test_simplify_expression_div(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Let([("x", Int(0))], Var("x")),
                SequentialNameGenerator(),
                sucrose.Let("x", Int(0), Var("x")),
            ),
        ]
    ),
)
def test_simplify_expression_let(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Var("x"),
                SequentialNameGenerator(),
                Var("x"),
            ),
        ]
    ),
)
def test_simplify_expression_var(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                LetStar([], Var("x")),
                SequentialNameGenerator(),
                Var("x"),
            ),
            (
                LetStar([("x", Int(0))], Var("x")),
                SequentialNameGenerator(),
                sucrose.Let("x", Int(0), Var("x")),
            ),
            (
                LetStar([("x", Int(0)), ("y", Int(1))], Var("x")),
                SequentialNameGenerator(),
                sucrose.Let(
                    "x",
                    Int(0),
                    sucrose.Let("y", Int(1), Var("x")),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_letstar(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Bool(True),
                SequentialNameGenerator(),
                Bool(True),
            ),
        ]
    ),
)
def test_simplify_expression_bool(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Not(Var("x")),
                SequentialNameGenerator(),
                If(sucrose.EqualTo(Var("x"), Bool(True)), Bool(False), Bool(True)),
            ),
        ]
    ),
)
def test_simplify_expression_not(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                And([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                And([Bool(True)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                And([Bool(True), Bool(False)]),
                SequentialNameGenerator(),
                If(Bool(True), Bool(False), Bool(False)),
            ),
        ]
    ),
)
def test_simplify_expression_and(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Or([]),
                SequentialNameGenerator(),
                Bool(False),
            ),
            (
                Or([Bool(True)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                Or([Bool(True), Bool(False)]),
                SequentialNameGenerator(),
                If(Bool(True), Bool(True), Bool(False)),
            ),
        ]
    ),
)
def test_simplify_expression_or(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                If(Bool(True), Var("x"), Var("y")),
                SequentialNameGenerator(),
                If(Bool(True), Var("x"), Var("y")),
            ),
        ]
    ),
)
def test_simplify_expression_if(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Cond([], Int(0)),
                SequentialNameGenerator(),
                Int(0),
            ),
            (
                Cond([(Bool(True), Int(1))], Int(0)),
                SequentialNameGenerator(),
                If(Bool(True), Int(1), Int(0)),
            ),
        ]
    ),
)
def test_simplify_expression_cond(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.LessThanOrEqualTo([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThanOrEqualTo([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThanOrEqualTo([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.GreaterThanOrEqualTo(Int(2), Int(1)),
            ),
            (
                fructose.LessThanOrEqualTo([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.GreaterThanOrEqualTo(Int(2), Int(1)),
                    sucrose.GreaterThanOrEqualTo(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_less_than_or_equal_to(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.LessThan([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThan([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.LessThan([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.LessThan(Int(1), Int(2)),
            ),
            (
                fructose.LessThan([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.LessThan(Int(1), Int(2)),
                    sucrose.LessThan(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_less_than(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.EqualTo([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.EqualTo([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.EqualTo([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.EqualTo(Int(1), Int(2)),
            ),
            (
                fructose.EqualTo([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.EqualTo(Int(1), Int(2)),
                    sucrose.EqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_equal_to(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.GreaterThan([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThan([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThan([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.LessThan(Int(2), Int(1)),
            ),
            (
                fructose.GreaterThan([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.LessThan(Int(2), Int(1)),
                    sucrose.LessThan(Int(3), Int(2)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_greater_than(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.GreaterThanOrEqualTo([]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(0)]),
                SequentialNameGenerator(),
                Bool(True),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(1), Int(2)]),
                SequentialNameGenerator(),
                sucrose.GreaterThanOrEqualTo(Int(1), Int(2)),
            ),
            (
                fructose.GreaterThanOrEqualTo([Int(1), Int(2), Int(3)]),
                SequentialNameGenerator(),
                If(
                    sucrose.GreaterThanOrEqualTo(Int(1), Int(2)),
                    sucrose.GreaterThanOrEqualTo(Int(2), Int(3)),
                    Bool(False),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_greater_than_or_equal_to(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Unit(),
                SequentialNameGenerator(),
                Unit(),
            ),
        ]
    ),
)
def test_simplify_expression_unit(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Cell(Unit()),
                SequentialNameGenerator(),
                Tuple([Unit()]),
            ),
        ]
    ),
)
def test_simplify_expression_cell(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Get(Var("x")),
                SequentialNameGenerator(),
                sucrose.Get(Var("x"), Int(0)),
            ),
        ]
    ),
)
def test_simplify_expression_get(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                fructose.Set(Var("x"), Var("y")),
                SequentialNameGenerator(),
                sucrose.Set(Var("x"), Int(0), Var("y")),
            ),
        ]
    ),
)
def test_simplify_expression_set(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                Begin([]),
                SequentialNameGenerator(),
                Unit(),
            ),
            (
                Begin([Int(0)]),
                SequentialNameGenerator(),
                Int(0),
            ),
            (
                Begin([Unit(), Int(0)]),
                SequentialNameGenerator(),
                Do(Unit(), Int(0)),
            ),
        ]
    ),
)
def test_simplify_expression_begin(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[fructose.Expression, Callable[[str], str], sucrose.Expression]](
        [
            (
                While(Var("x"), Var("y")),
                SequentialNameGenerator(),
                sucrose.Let[sucrose.Expression, sucrose.Expression](
                    "_loop0",
                    Unit(),
                    Do(
                        Assign("_loop0", Lambda([], If(Var("x"), Do(Var("y"), Apply(Var("_loop0"), [])), Unit()))),
                        Apply(Var("_loop0"), []),
                    ),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_while(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh, expected",
    list[tuple[Expression, Callable[[str], str], sucrose.Expression]](
        [
            # Empty match - defaults to Unit
            (
                fructose.Match(Int(1), []),  # type: ignore
                SequentialNameGenerator(),
                sucrose.Unit(),
            ),
            # Integer pattern matching
            (
                fructose.Match(Int(1), [(fructose.PatternInt(1), Int(42))]),
                SequentialNameGenerator(),
                sucrose.If(sucrose.EqualTo(Int(1), sucrose.Int(1)), Int(42), sucrose.Unit()),
            ),
            # Boolean pattern matching
            (
                fructose.Match(Bool(True), [(fructose.PatternTrue(), Int(1))]),
                SequentialNameGenerator(),
                sucrose.If(sucrose.EqualTo(Bool(True), sucrose.Bool(True)), Int(1), sucrose.Unit()),
            ),
            (
                fructose.Match(Bool(False), [(fructose.PatternFalse(), Int(0))]),
                SequentialNameGenerator(),
                sucrose.If(sucrose.EqualTo(Bool(False), sucrose.Bool(False)), Int(0), sucrose.Unit()),
            ),
            # Unit pattern matching
            (
                fructose.Match(Unit(), [(fructose.PatternUnit(), Int(1))]),
                SequentialNameGenerator(),
                sucrose.If(sucrose.EqualTo(Unit(), sucrose.Unit()), Int(1), sucrose.Unit()),
            ),
            # Variable binding pattern
            (
                fructose.Match(Int(42), [(fructose.PatternVar("x"), Var("x"))]),
                SequentialNameGenerator(),
                sucrose.Let("x", Int(42), Var("x")),
            ),
            # Wildcard pattern
            (
                fructose.Match(Int(42), [(fructose.PatternWildcard(), Int(1))]),
                SequentialNameGenerator(),
                Int(1),
            ),
            # Need to fix the tuple pattern matching
            # # Tuple pattern matching
            # (
            #     fructose.Match(
            #         Tuple([Int(1), Int(2)]),
            #         [(fructose.PatternCons("tuple", [fructose.PatternInt(1), fructose.PatternInt(2)]), Int(3))]
            #     ),
            #     SequentialNameGenerator(),
            #     sucrose.If(
            #         sucrose.EqualTo(Tuple([Int(1), Int(2)]), Tuple([sucrose.Int(1), sucrose.Int(2)])),
            #         Int(3),
            #         sucrose.Unit()
            #     ),
            # ),
            # Multiple patterns
            (
                fructose.Match(
                    Int(1),
                    [
                        (fructose.PatternInt(0), Int(0)),
                        (fructose.PatternInt(1), Int(1)),
                        (fructose.PatternWildcard(), Int(2)),
                    ],
                ),
                SequentialNameGenerator(),
                sucrose.If(
                    sucrose.EqualTo(Int(1), sucrose.Int(0)),
                    Int(0),
                    sucrose.If(sucrose.EqualTo(Int(1), sucrose.Int(1)), Int(1), Int(2)),
                ),
            ),
        ]
    ),
)
def test_simplify_expression_match(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
    expected: sucrose.Expression,
) -> None:
    assert simplify_expression(expr, fresh) == expected


@pytest.mark.parametrize(
    "expr, fresh",
    [
        # Test unsupported constructor
        (
            fructose.Match(Int(1), [(fructose.PatternCons("unsupported", []), Int(1))]),
            SequentialNameGenerator(),
        ),
        # Test unsupported pattern type
        (
            fructose.Match(
                Int(1),
                [(object(), Int(1))],  # type: ignore
            ),
            SequentialNameGenerator(),
        ),
    ],
)
def test_simplify_expression_match_errors(
    expr: fructose.Expression,
    fresh: Callable[[str], str],
) -> None:
    with pytest.raises(NotImplementedError):
        simplify_expression(expr, fresh)
