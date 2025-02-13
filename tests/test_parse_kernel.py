import pytest
from kernel import Expression, Int, Add, Subtract, Multiply, Let, Var, Bool, If, Compare
from parse_kernel import parse_expr


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Int]](
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
    list[tuple[str, Add]](
        [
            (
                "(+ 1 2)",
                Add(Int(1), Int(2)),
            ),
        ]
    ),
)
def test_parse_expr_add(
    source: str,
    expected: Add,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Subtract]](
        [
            (
                "(- 2 1)",
                Subtract(Int(2), Int(1)),
            ),
        ]
    ),
)
def test_parse_expr_subtract(
    source: str,
    expected: Subtract,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Multiply]](
        [
            (
                "(* 1 2)",
                Multiply(Int(1), Int(2)),
            ),
        ]
    ),
)
def test_parse_expr_multiply(
    source: str,
    expected: Multiply,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Let]](
        [
            (
                "(let ([x 1]) x)",
                Let("x", Int(1), Var("x")),
            ),
        ]
    ),
)
def test_parse_expr_let(
    source: str,
    expected: Let,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Var]](
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
    expected: Var,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Bool]](
        [
            (
                "true",
                Bool(True),
            ),
            (
                "false",
                Bool(False),
            ),
        ]
    ),
)
def test_parse_expr_bool(
    source: str,
    expected: Bool,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, If]](
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
    expected: If,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Compare]](
        [
            (
                "(< 1 0)",
                Compare("<", Int(1), Int(0)),
            ),
            (
                "(== 1 0)",
                Compare("==", Int(1), Int(0)),
            ),
            (
                "(>= 1 0)",
                Compare(">=", Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_compare(
    source: str,
    expected: Expression,
) -> None:
    assert parse_expr(source) == expected
