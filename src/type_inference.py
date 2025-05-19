from __future__ import annotations
from typing import Dict, List, Set
from fructose import (
    Program, Expression, Int, Var, Bool, Not, And, Or, If, Cond, Unit, Lambda, Apply, Let, LetStar, LetRec, Assign, Subtract, Add, Multiply, Div, LessThanOrEqualTo, LessThan, EqualTo, GreaterThan, GreaterThanOrEqualTo, Cell, Get, Set, Begin, While
)
import builtins

# --- Type System ---
class Type:
    pass

class TypeVar(Type):
    _next_id = 0
    def __init__(self):
        self.id = TypeVar._next_id
        TypeVar._next_id += 1
    def __repr__(self):
        return f"t{self.id}"
    def __eq__(self, other: object) -> bool:
        return isinstance(other, TypeVar) and self.id == other.id
    def __hash__(self):
        return hash(self.id)

class IntType(Type):
    def __repr__(self): return "Int"
    def __eq__(self, other: object) -> bool: return isinstance(other, IntType)
    def __hash__(self): return hash("IntType")

class BoolType(Type):
    def __repr__(self): return "Bool"
    def __eq__(self, other: object) -> bool: return isinstance(other, BoolType)
    def __hash__(self): return hash("BoolType")

class UnitType(Type):
    def __repr__(self): return "Unit"
    def __eq__(self, other: object) -> bool: return isinstance(other, UnitType)
    def __hash__(self): return hash("UnitType")

class FunType(Type):
    def __init__(self, arg_types: List[Type], ret_type: Type):
        self.arg_types = arg_types
        self.ret_type = ret_type
    def __repr__(self):
        return f"({' -> '.join(map(str, self.arg_types))} -> {self.ret_type})"
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FunType)
            and self.arg_types == other.arg_types
            and self.ret_type == other.ret_type
        )
    def __hash__(self):
        return hash((tuple(self.arg_types), self.ret_type))

# --- Type Environment ---
TypeEnv = Dict[str, Type]

# --- Unification ---
class TypeError(Exception):
    pass

def occurs_check(tv: TypeVar, t: Type, subst: Dict[TypeVar, Type]) -> bool:
    t = prune(t, subst)
    if t == tv:
        return True
    elif isinstance(t, FunType):
        return any(occurs_check(tv, arg, subst) for arg in t.arg_types) or occurs_check(tv, t.ret_type, subst)
    else:
        return False

def prune(t: Type, subst: Dict[TypeVar, Type]) -> Type:
    if isinstance(t, TypeVar) and t in subst:
        real = prune(subst[t], subst)
        subst[t] = real
        return real
    return t

def unify(t1: Type, t2: Type, subst: Dict[TypeVar, Type]):
    t1 = prune(t1, subst)
    t2 = prune(t2, subst)
    if isinstance(t1, TypeVar):
        if t1 != t2:
            if occurs_check(t1, t2, subst):
                raise TypeError(f"Recursive unification: {t1} and {t2}")
            subst[t1] = t2
    elif isinstance(t2, TypeVar):
        unify(t2, t1, subst)
    elif type(t1) == type(t2):
        if isinstance(t1, (IntType, BoolType, UnitType)):
            pass
        elif isinstance(t1, FunType) and isinstance(t2, FunType):
            if len(t1.arg_types) != len(t2.arg_types):
                raise TypeError(f"Function arity mismatch: {t1} vs {t2}")
            for a, b in zip(t1.arg_types, t2.arg_types):
                unify(a, b, subst)
            unify(t1.ret_type, t2.ret_type, subst)
        else:
            raise TypeError(f"Unknown type for unification: {t1}")
    else:
        raise TypeError(f"Type mismatch: {t1} vs {t2}")

# --- Generalization/Instantiation ---
def free_type_vars(t: Type, subst: Dict[TypeVar, Type]) -> builtins.set[TypeVar]:
    t = prune(t, subst)
    if isinstance(t, TypeVar):
        return builtins.set([t])
    elif isinstance(t, FunType):
        s: builtins.set[TypeVar] = builtins.set()
        for arg in t.arg_types:
            s.update(builtins.set(list(free_type_vars(arg, subst))))
        s.update(builtins.set(list(free_type_vars(t.ret_type, subst))))
        return s
    else:
        return builtins.set()

def free_type_vars_env(env: TypeEnv, subst: Dict[TypeVar, Type]) -> builtins.set[TypeVar]:
    s: builtins.set[TypeVar] = builtins.set()
    for t in env.values():
        s.update(builtins.set(list(free_type_vars(t, subst))))
    return s

def generalize(t: Type, env: TypeEnv, subst: Dict[TypeVar, Type]) -> Type:
    # For simplicity, we do not implement explicit polymorphism in this first version
    return t

def instantiate(t: Type, subst: Dict[TypeVar, Type]) -> Type:
    # For simplicity, we do not implement explicit polymorphism in this first version
    return t

# --- Type Inference ---
def infer_expr(expr: Expression, env: TypeEnv, subst: Dict[TypeVar, Type]) -> Type:
    if isinstance(expr, Int):
        return IntType()
    if isinstance(expr, Bool):
        return BoolType()
    if isinstance(expr, Unit):
        return UnitType()
    if isinstance(expr, Var):
        if expr.name not in env:
            raise TypeError(f"Unbound variable: {expr.name}")
        return instantiate(env[expr.name], subst)
    if isinstance(expr, Add) or isinstance(expr, Subtract) or isinstance(expr, Multiply) or isinstance(expr, Div):
        # All operands must be Int
        for arg in expr.operands:
            t = infer_expr(arg, env, subst)
            unify(t, IntType(), subst)
        return IntType()
    if isinstance(expr, And) or isinstance(expr, Or):
        for arg in expr.operands:
            t = infer_expr(arg, env, subst)
            unify(t, BoolType(), subst)
        return BoolType()
    if isinstance(expr, Not):
        t = infer_expr(expr.operand, env, subst)
        unify(t, BoolType(), subst)
        return BoolType()
    if isinstance(expr, If):
        t_cond = infer_expr(expr.condition, env, subst)
        unify(t_cond, BoolType(), subst)
        t_then = infer_expr(expr.consequent, env, subst)
        t_else = infer_expr(expr.alternative, env, subst)
        unify(t_then, t_else, subst)
        return t_then
    if isinstance(expr, Let):
        new_env = env.copy()
        for name, value in expr.bindings:
            t_val = infer_expr(value, env, subst)
            new_env[name] = generalize(t_val, env, subst)
        return infer_expr(expr.body, new_env, subst)
    if isinstance(expr, LetStar):
        new_env = env.copy()
        for name, value in expr.bindings:
            t_val = infer_expr(value, new_env, subst)
            new_env[name] = generalize(t_val, new_env, subst)
        return infer_expr(expr.body, new_env, subst)
    if isinstance(expr, LetRec):
        new_env = env.copy()
        # Pre-bind all names to fresh type vars
        for name, _ in expr.bindings:
            new_env[name] = TypeVar()
        # Now infer and unify
        for name, value in expr.bindings:
            t_val = infer_expr(value, new_env, subst)
            unify(new_env[name], t_val, subst)
        return infer_expr(expr.body, new_env, subst)
    if isinstance(expr, Lambda):
        param_types: List[Type] = [TypeVar() for _ in expr.parameters]
        new_env = env.copy()
        for name, t in zip(expr.parameters, param_types):
            new_env[name] = t
        t_body = infer_expr(expr.body, new_env, subst)
        return FunType(param_types, t_body)
    if isinstance(expr, Apply):
        t_fun = infer_expr(expr.callee, env, subst)
        arg_types = [infer_expr(arg, env, subst) for arg in expr.arguments]
        t_ret = TypeVar()
        unify(t_fun, FunType(arg_types, t_ret), subst)
        return t_ret
    if isinstance(expr, Assign):
        # Assignment is only allowed for variables already in the environment
        if expr.name not in env:
            raise TypeError(f"Assignment to unbound variable: {expr.name}")
        t_val = infer_expr(expr.value, env, subst)
        unify(env[expr.name], t_val, subst)
        return UnitType()
    if isinstance(expr, Cond):
        # Each arm is (cond, expr)
        t_result = TypeVar()
        for cond, val in expr.arms:
            t_cond = infer_expr(cond, env, subst)
            unify(t_cond, BoolType(), subst)
            t_arm = infer_expr(val, env, subst)
            unify(t_result, t_arm, subst)
        t_default = infer_expr(expr.default, env, subst)
        unify(t_result, t_default, subst)
        return t_result
    if isinstance(expr, LessThanOrEqualTo) or isinstance(expr, LessThan) or isinstance(expr, EqualTo) or isinstance(expr, GreaterThan) or isinstance(expr, GreaterThanOrEqualTo):
        for arg in expr.operands:
            t = infer_expr(arg, env, subst)
            unify(t, IntType(), subst)
        return BoolType()
    if isinstance(expr, Cell):
        # Mutable cell, just check the value
        infer_expr(expr.value, env, subst)
        return UnitType()
    if isinstance(expr, Get):
        # For now, just check the cell
        infer_expr(expr.cell, env, subst)
        return IntType()  # Could be more general
    if isinstance(expr, Set):
        infer_expr(expr.cell, env, subst)
        infer_expr(expr.value, env, subst)
        return UnitType()
    if isinstance(expr, Begin):
        t = UnitType()
        for e in expr.operands:
            t = infer_expr(e, env, subst)
        return t
    if isinstance(expr, While):
        t_cond = infer_expr(expr.condition, env, subst)
        unify(t_cond, BoolType(), subst)
        infer_expr(expr.body, env, subst)
        return UnitType()
    raise TypeError(f"Unknown expression: {expr}")

def infer_types(program: Program) -> Dict[str, Type]:
    subst: Dict[TypeVar, Type] = {}
    env: TypeEnv = {param: TypeVar() for param in program.parameters}
    t_body = infer_expr(program.body, env, subst)
    # Return the types of parameters and the program result
    result = {param: prune(t, subst) for param, t in env.items()}
    result["$result"] = prune(t_body, subst)
    return result

# For testing: TypeError is raised on type errors
