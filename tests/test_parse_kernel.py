import pytest
from kernel import Int, Binary, Let, Var, Bool, If
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
    list[tuple[str, Binary]](
        [
            (
                "(+ 1 2)",
                Binary("+", Int(1), Int(2)),
            ),
        ]
    ),
)
def test_parse_expr_int_add(
    source: str,
    expected: Binary,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Binary]](
        [
            (
                "(- 2 1)",
                Binary("-", Int(2), Int(1)),
            ),
        ]
    ),
)
def test_parse_expr_int_subtract(
    source: str,
    expected: Binary,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Binary]](
        [
            (
                "(* 1 2)",
                Binary("*", Int(1), Int(2)),
            ),
        ]
    ),
)
def test_parse_expr_multiply(
    source: str,
    expected: Binary,
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
                "#t",
                Bool(True),
            ),
            (
                "#f",
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
    list[tuple[str, Binary]](
        [
            (
                "(< 1 0)",
                Binary("<", Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_less_than(
    source: str,
    expected: Binary,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Binary]](
        [
            (
                "(== 1 0)",
                Binary("==", Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_equal_to(
    source: str,
    expected: Binary,
) -> None:
    assert parse_expr(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    list[tuple[str, Binary]](
        [
            (
                "(>= 1 0)",
                Binary(">=", Int(1), Int(0)),
            ),
        ]
    ),
)
def test_parse_expr_greater_than_or_equal_to(
    source: str,
    expected: Binary,
) -> None:
    assert parse_expr(source) == expected
