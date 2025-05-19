import pytest
from fructose import *
from type_inference import infer_types, TypeError, IntType, BoolType, UnitType
from type_inference import FunType, TypeVar, unify

def test_int():
    prog = Program([], Int(42))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_bool():
    prog = Program([], Bool(True))
    types = infer_types(prog)
    assert types["$result"] == BoolType()

def test_unit():
    prog = Program([], Unit())
    types = infer_types(prog)
    assert types["$result"] == UnitType()

def test_add():
    prog = Program([], Add([Int(1), Int(2)]))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_and():
    prog = Program([], And([Bool(True), Bool(False)]))
    types = infer_types(prog)
    assert types["$result"] == BoolType()

def test_if():
    prog = Program([], If(Bool(True), Int(1), Int(2)))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_if_type_error():
    prog = Program([], If(Int(1), Int(1), Int(2)))
    with pytest.raises(TypeError):
        infer_types(prog)

def test_let():
    prog = Program([], Let([("x", Int(1))], Add([Var("x"), Int(2)])))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_let_shadow():
    prog = Program([], Let([("x", Int(1))], Let([("x", Bool(True))], Var("x"))))
    types = infer_types(prog)
    assert types["$result"] == BoolType()

def test_letrec():
    # letrec f = (lambda (x) (if (= x 0) 1 (f (- x 1)))) in (f 5)
    f = "f"
    lam = Lambda(["x"], If(EqualTo([Var("x"), Int(0)]), Int(1), Apply(Var(f), [Subtract([Var("x"), Int(1)])])))
    prog = Program([], LetRec([(f, lam)], Apply(Var(f), [Int(5)])))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_lambda_apply():
    lam = Lambda(["x"], Add([Var("x"), Int(1)]))
    prog = Program([], Apply(lam, [Int(2)]))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_higher_order():
    # (lambda (f) (f 1))
    lam = Lambda(["f"], Apply(Var("f"), [Int(1)]))
    prog = Program([], lam)
    types = infer_types(prog)
    result_type = types["$result"]
    assert isinstance(result_type, FunType), f"Expected FunType, got {result_type}"
    # The argument type should be unifiable with FunType([IntType()], t)
    subst = {}
    try:
        unify(result_type.arg_types[0], FunType([IntType()], TypeVar()), subst)
    except Exception as e:
        assert False, f"Argument type {result_type.arg_types[0]} is not unifiable with FunType([IntType()], t): {e}"

def test_apply_type_error():
    lam = Lambda(["x"], Add([Var("x"), Int(1)]))
    prog = Program([], Apply(lam, [Bool(True)]))
    with pytest.raises(TypeError):
        infer_types(prog)

def test_unbound_var():
    prog = Program([], Var("x"))
    with pytest.raises(TypeError):
        infer_types(prog)

def test_arity_mismatch():
    lam = Lambda(["x", "y"], Add([Var("x"), Var("y")]))
    prog = Program([], Apply(lam, [Int(1)]))
    with pytest.raises(TypeError):
        infer_types(prog)

def test_recursive_type_error():
    # let x = x in x
    prog = Program([], Let([("x", Var("x"))], Var("x")))
    with pytest.raises(TypeError):
        infer_types(prog)

def test_cond():
    prog = Program([], Cond([(Bool(True), Int(1)), (Bool(False), Int(2))], Int(3)))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_begin():
    prog = Program([], Begin([Int(1), Int(2), Int(3)]))
    types = infer_types(prog)
    assert types["$result"] == IntType()

def test_while():
    prog = Program([], While(Bool(True), Int(1)))
    types = infer_types(prog)
    assert types["$result"] == UnitType()

def test_assign():
    prog = Program(["x"], Assign("x", Int(2)))
    types = infer_types(prog)
    assert types["$result"] == UnitType()

def test_cell_get_set():
    prog = Program([], Begin([Cell(Int(1)), Get(Int(1)), Set(Int(1), Int(2))]))
    types = infer_types(prog)
    assert types["$result"] == UnitType() or types["$result"] == IntType()