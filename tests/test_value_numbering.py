import pytest
from value_numbering import value_numbering, VNError
from glucose import Program, Int, Bool, Var, Add

def test_vn_simple_expression():
    # let v0 = (x + y) in v0
    body = Add(Var("x"), Var("y"))
    prog = Program(["x", "y"], body)
    vn = value_numbering(prog)
    from glucose import Let, Var as GVar
    # After VN, body must be a Let binding
    assert isinstance(vn.body, Let)
    assert vn.body.name.startswith("v")
    assert isinstance(vn.body.value, Add)
    assert isinstance(vn.body.body, GVar)
    assert vn.body.body.name == vn.body.name

def test_vn_duplicate_literals():
    # (2+3) and (2+3) → only one global binding
    expr = Add(Add(Int(2), Int(3)), Add(Int(2), Int(3)))
    prog = Program([], expr)
    vn = value_numbering(prog)
    from glucose import Let, Var as GVar
    # The first binding should be named v0
    let1 = vn.body
    assert isinstance(let1, Let)
    assert let1.name == "v0"
    # The body of v0's Let should be the top-level Add(...)
    assert isinstance(let1.value, Add)
    # And the final body must be Var('v0')
    assert isinstance(let1.body, GVar)
    assert let1.body.name == "v0"

def test_vn_error_on_unrecognized():
    # Passing a Bool (which VN doesn't handle) should error
    prog = Program([], Bool(True))
    with pytest.raises(VNError):
        value_numbering(prog)

def test_pipeline_constant_fold_then_vn():
    # ((3*0) + (4/2)) → ((0) + 2) → 2
    from constant_folding import constant_fold
    from glucose import Multiply, Div
    expr = Add(Multiply(Int(3), Int(0)), Div(Int(4), Int(2)))
    prog = Program([], expr)
    folded = constant_fold(prog)
    vn = value_numbering(folded)
    # after VN: let v0 = 2 in v0 (or just Int(2), depending on VN implementation)
    # Accept either Int(2) or a Let binding to Int(2)
    if isinstance(vn.body, Int):
        assert vn.body.value == 2
    else:
        # If value numbering introduces a let binding
        assert hasattr(vn.body, "name")
        assert isinstance(vn.body.value, Int) and vn.body.value.value == 2
        assert isinstance(vn.body.body, Var) and vn.body.body.name == vn.body.name 