import pytest
from fructose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    LetStar,
    LetRec,
    Var,
    Bool,
    Not,
    And,
    Or,
    If,
    Cond,
    LessThanOrEqualTo,
    LessThan,
    EqualTo,
    GreaterThan,
    GreaterThanOrEqualTo,
    Unit,
    Cell,
    Get,
    Set,
    Begin,
    While,
    Lambda,
    Apply,
    Assign,
)
from parse import parse, parse_expr


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Program]](
        [
            (
                "(program () 0)",
                Program([], Int(0)),
            ),
            (
                "(program (x) x)",
                Program(["x"], Var("x")),
            ),
        ]
    ),
)
def test_parse(
    source: str,
    expected: Program,
) -> None:
    assert parse(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "0",
                Int(0),
            ),
        ]
    ),
)
def test_parse_expr_int(
    source: str,
    expected: Int,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(+)",
                Add([]),
            ),
            (
                "(+ 1 2)",
                Add([Int(1), Int(2)]),
            ),
        ]
    ),
)
def test_parse_expr_add(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(- 1)",
                Subtract([Int(1)]),
            ),
            (
                "(- 2 1)",
                Subtract([Int(2), Int(1)]),
            ),
        ]
    ),
)
def test_parse_expr_subtract(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(*)",
                Multiply([]),
            ),
            (
                "(* 1 2)",
                Multiply([Int(1), Int(2)]),
            ),
        ]
    ),
)
def test_parse_expr_multiply(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(let () x)",
                Let([], Var("x")),
            ),
            (
                "(let ((x 1)) x)",
                Let([("x", Int(1))], Var("x")),
            ),
        ]
    ),
)
def test_parse_expr_let(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(let* () x)",
                LetStar([], Var("x")),
            ),
            (
                "(let* ((x 1)) x)",
                LetStar([("x", Int(1))], Var("x")),
            ),
        ]
    ),
)
def test_parse_expr_letstar(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(letrec () x)",
                LetRec([], Var("x")),
            ),
            (
                "(letrec ((x 1)) x)",
                LetRec([("x", Int(1))], Var("x")),
            ),
        ]
    ),
)
def test_parse_expr_letrec(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "x",
                Var("x"),
            ),
        ]
    ),
)
def test_parse_expr_var(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "#t",
                Bool(True),
            ),
        ]
    ),
)
def test_parse_expr_true(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "#f",
                Bool(False),
            ),
        ]
    ),
)
def test_parse_expr_false(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(not #t)",
                Not(Bool(True)),
            ),
        ]
    ),
)
def test_parse_expr_not(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(and)",
                And([]),
            ),
            (
                "(and #t #t)",
                And([Bool(True), Bool(True)]),
            ),
        ]
    ),
)
def test_parse_expr_and(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(or)",
                Or([]),
            ),
            (
                "(or #t #t)",
                Or([Bool(True), Bool(True)]),
            ),
        ]
    ),
)
def test_parse_expr_or(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(if x 1 0)",
                If(Var("x"), Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_if(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(cond #u)",
                Cond([], Unit()),
            ),
            (
                "(cond (x y) #u)",
                Cond([(Var("x"), Var("y"))], Unit()),
            ),
        ]
    ),
)
def test_parse_expr_cond(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(<=)",
                LessThanOrEqualTo([]),
            ),
            (
                "(<= 1 0)",
                LessThanOrEqualTo([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expr_less_than_or_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(<)",
                LessThan([]),
            ),
            (
                "(< 1 0)",
                LessThan([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expr_less_than(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(=)",
                EqualTo([]),
            ),
            (
                "(= 1 0)",
                EqualTo([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expr_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(>)",
                GreaterThan([]),
            ),
            (
                "(> 1 0)",
                GreaterThan([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expr_greater_than(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(>=)",
                GreaterThanOrEqualTo([]),
            ),
            (
                "(>= 1 0)",
                GreaterThanOrEqualTo([Int(1), Int(0)]),
            ),
        ]
    ),
)
def test_parse_expr_greater_than_or_equal_to(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "#u",
                Unit(),
            ),
        ]
    ),
)
def test_parse_expr_unit(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(cell #u)",
                Cell(Unit()),
            ),
        ]
    ),
)
def test_parse_expr_cell(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(^ x)",
                Get(Var("x")),
            ),
        ]
    ),
)
def test_parse_expr_get(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(:= x #u)",
                Set(Var("x"), Unit()),
            ),
        ]
    ),
)
def test_parse_expr_set(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(begin)",
                Begin([]),
            ),
            (
                "(begin #u)",
                Begin([Unit()]),
            ),
        ]
    ),
)
def test_parse_expr_begin(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(while #t #u)",
                While(Bool(True), Unit()),
            ),
        ]
    ),
)
def test_parse_expr_while(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(abs () 0)",
                Lambda([], Int(0)),
            ),
            (
                "(abs (x) x)",
                Lambda(["x"], Var("x")),
            ),
        ]
    ),
)
def test_parse_expr_lambda(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(x)",
                Apply(Var("x"), []),
            ),
        ]
    ),
)
def test_parse_expr_apply(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Expression]](
        [
            (
                "(set! x #u)",
                Assign("x", Unit()),
            ),
        ]
    ),
)
def test_parse_expr_assign(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected
