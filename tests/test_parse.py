import pytest
from fructose import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Div,
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
    Match,
    PatternInt,
    PatternTrue,
    PatternFalse,
    PatternUnit,
    PatternWildcard,
    PatternVar,
    PatternCons
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
                "(/ 2 1)",
                Div([Int(2), Int(1)]),
            ),
        ]
    ),
)
def test_parse_expr_div(
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

# TESTS FOR PATTERN MATCHING 
def test_parse_match_literal():
    src = """
    (match 42
      (42 "forty-two")
      (0 "zero")
      (_ "other"))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[0][0], PatternInt)
    assert ast.arms[0][0].value == 42


def test_parse_match_bool():
    src = """
    (match #t
      (#t "true")
      (#f "false")
      (_ "other"))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[0][0], PatternTrue)
    assert isinstance(ast.arms[1][0], PatternFalse)


def test_parse_match_unit():
    src = """
    (match #u
      (#u "unit")
      (_ "other"))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[0][0], PatternUnit)


def test_parse_match_wildcard():
    src = """
    (match 99
      (0 "zero")
      (_ "not zero"))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[-1][0], PatternWildcard)


def test_parse_match_var():
    src = """
    (match 7
      (x x)
      (_ "no match"))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[0][0], PatternVar)
    assert ast.arms[0][0].name == "x"


def test_parse_match_tuple_flat():
    src = """
    (match (tuple 1 2)
      ((tuple x y) (+ x y))
      (_ 0))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[0][0], PatternCons)
    assert ast.arms[0][0].constructor == "tuple"
    assert len(ast.arms[0][0].patterns) == 2


def test_parse_match_tuple_nested():
    src = """
    (match (tuple 1 (tuple 2 3))
      ((tuple x (tuple y z)) (+ x (+ y z)))
      (_ 0))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    pat = ast.arms[0][0]
    assert isinstance(pat, PatternCons)
    assert pat.constructor == "tuple"
    assert isinstance(pat.patterns[1], PatternCons)
    assert pat.patterns[1].constructor == "tuple"


def test_parse_match_tuple_with_literals_and_wildcard():
    src = """
    (match (tuple 1 2)
      ((tuple 1 _) "first is one")
      ((tuple _ 2) "second is two")
      (_ "no match"))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[0][0].patterns[0], PatternInt)
    assert ast.arms[0][0].patterns[0].value == 1
    assert isinstance(ast.arms[0][0].patterns[1], PatternWildcard)


def test_parse_match_tuple_with_var_and_literal():
    src = """
    (match (tuple 5 0)
      ((tuple x 0) x)
      (_ -1))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    assert isinstance(ast.arms[0][0].patterns[1], PatternInt)
    assert ast.arms[0][0].patterns[1].value == 0
    assert isinstance(ast.arms[0][0].patterns[0], PatternVar)


def test_parse_match_nested_tuple_with_wildcard_and_var():
    src = """
    (match (tuple (tuple 1 2) 3)
      ((tuple (tuple _ y) z) (+ y z))
      (_ 0))
    """
    ast = parse_expr(src)
    assert isinstance(ast, Match)
    pat = ast.arms[0][0]
    assert isinstance(pat, PatternCons)
    assert pat.constructor == "tuple"
    assert isinstance(pat.patterns[0], PatternCons)
    assert pat.patterns[0].constructor == "tuple"
    assert isinstance(pat.patterns[0].patterns[0], PatternWildcard)
    assert isinstance(pat.patterns[0].patterns[1], PatternVar)
