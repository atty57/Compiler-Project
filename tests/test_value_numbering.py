import pytest
from value_numbering import value_numbering, VNError
from glucose import Program, Int, Bool, Var, Add
from typing import Any


@pytest.mark.parametrize(  # type: ignore
    "prog, check",
    [
        (
            Program(["x", "y"], Add(Var("x"), Var("y"))),  # type: ignore
            lambda vn: (
                hasattr(vn.body, "name")
                and vn.body.name.startswith("v")  # type: ignore
                and isinstance(vn.body.value, Add)  # type: ignore
                and hasattr(vn.body.body, "name")  # type: ignore
                and vn.body.body.name == vn.body.name  # type: ignore
            ),  # type: ignore
        ),
        (
            Program([], Add(Add(Int(2), Int(3)), Add(Int(2), Int(3)))),  # type: ignore
            lambda vn: (
                hasattr(vn.body, "name")
                and vn.body.name == "v0"  # type: ignore
                and isinstance(vn.body.value, Add)  # type: ignore
                and hasattr(vn.body.body, "name")  # type: ignore
                and vn.body.body.name == "v0"  # type: ignore
            ),  # type: ignore
        ),
    ],
)
def test_value_numbering(prog: Any, check: Any) -> None:  # type: ignore
    vn = value_numbering(prog)
    assert check(vn)


def test_vn_error_on_unrecognized() -> None:
    prog = Program([], Bool(True))
    with pytest.raises(VNError):
        value_numbering(prog)


def test_pipeline_constant_fold_then_vn() -> None:
    from constant_folding import constant_fold
    from glucose import Multiply, Div

    expr = Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))  # type: ignore
    prog = Program([], expr)
    folded = constant_fold(prog)
    vn = value_numbering(folded)
    if isinstance(vn.body, Int):
        assert vn.body.value == 2
    else:
        assert hasattr(vn.body, "name")
        assert isinstance(vn.body.value, Int) and vn.body.value.value == 2  # type: ignore
        child = getattr(vn.body, "body", None)
        assert child is not None and hasattr(child, "name")
        assert child.name == vn.body.name  # type: ignore
