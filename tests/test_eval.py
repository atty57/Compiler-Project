import pytest
from kernel import Expression, Int, Add, Subtract, Multiply, Let, Var
from eval import Value, Environment, eval_expr


@pytest.mark.parametrize(
    "expr, env, expected",
    list[tuple[Expression, Environment, Value]](
        [
            # Int
            (
                Int(0),
                {},
                0,
            ),
            # Add
            (
                Add(Int(1), Int(1)),
                {},
                2,
            ),
            # Subtract
            (
                Subtract(Int(1), Int(1)),
                {},
                0,
            ),
            # Multiply
            (
                Multiply(Int(1), Int(2)),
                {},
                2,
            ),
            # Let
            (
                Let("x", Int(1), Var("x")),
                {},
                1,
            ),
            # Var
            (
                Var("x"),
                {"x": 0},
                0,
            ),
        ]
    ),
)
def test_eval_expr(
    expr: Expression,
    env: Environment,
    expected: int,
) -> None:
    assert eval_expr(expr, env) == expected
