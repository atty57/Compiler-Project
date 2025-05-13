import pytest
from value_numbering import value_numbering, VNError
from glucose import Program, Int, Bool, Var, Add
from typing import Any, Callable

@pytest.mark.parametrize(
    "prog, check",
    [
        (
            Program(["x", "y"], Add(Var("x"), Var("y"))),
            lambda vn: (
                hasattr(vn.body, "name")
                and vn.body.name.startswith("v")
                and isinstance(vn.body.value, Add)
                and hasattr(vn.body.body, "name")
                and vn.body.body.name == vn.body.name
            ),
        ),
        (
            Program([], Add(Add(Int(2), Int(3)), Add(Int(2), Int(3)))),
            lambda vn: (
                hasattr(vn.body, "name")
                and vn.body.name == "v0"
                and isinstance(vn.body.value, Add)
                and hasattr(vn.body.body, "name")
                and vn.body.body.name == "v0"
            ),
        ),
    ]
)
def test_value_numbering(prog: Program, check: Callable[[Any], bool]) -> None:
    vn = value_numbering(prog)
    assert check(vn)

def test_vn_error_on_unrecognized() -> None:
    prog = Program([], Bool(True))
    with pytest.raises(VNError):
        value_numbering(prog)

def test_pipeline_constant_fold_then_vn() -> None:
    from constant_folding import constant_fold
    from glucose import Multiply, Div
    expr = Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))
    prog = Program([], expr)
    folded = constant_fold(prog)
    vn = value_numbering(folded)
    # Accept either Int(2) or a Let binding to Int(2)
    if isinstance(vn.body, Int):
        assert vn.body.value == 2
    else:
        assert hasattr(vn.body, "name")
        assert isinstance(vn.body.value, Int) and vn.body.value.value == 2
        assert hasattr(vn.body.body, "name")
        assert vn.body.body.name == vn.body.name 