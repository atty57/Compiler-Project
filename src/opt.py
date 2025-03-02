from functools import partial
from kernel import (
    Program,
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
    Bool,
    If,
    LessThan,
    EqualTo,
    GreaterThanOrEqualTo,
    Unit,
    Cell,
    Get,
    Set,
    Do,
    While,
)

def opt(
    program: Program,
) -> Program:
    return Program(
        parameters=program.parameters,
        body=opt_expr(program.body),
    )

def opt_expr(
    expr: Expression,
) -> Expression:
    recur = partial(opt_expr)

    match expr:
        case Int():
            return expr

        case Unit():
            return expr

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [Int(0), e2_]:
                    return e2_
                case [e1_, Int(0)]:
                    return e1_
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)
                case [Int(i1), Add(Int(i2), e2_)]:
                    return Add(Int(i1 + i2), e2_)
                case [Add(Int(i1), e1_), Add(Int(i2), e2_)]:
                    return Add(Int(i1 + i2), Add(e1_, e2_))
                case [e1_, Int() as e2_]:
                    return Add(e2_, e1_)
                case [e1_, e2_]:
                    return Add(e1_, e2_)

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 - i2)
                case [e1_, e2_]:
                    return Subtract(e1_, e2_)

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [Int(0), _]:
                    return Int(0)
                case [_, Int(0)]:
                    return Int(0)
                case [Int(1), e2_]:
                    return e2_
                case [e1_, Int(1)]:
                    return e1_
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)
                case [Int(i1), Multiply(Int(i2), e2_)]:
                    return Multiply(Int(i1 * i2), e2_)
                case [Multiply(Int(i1), e1_), Multiply(Int(i2), e2_)]:
                    return Multiply(Int(i1 * i2), Multiply(e1_, e2_))
                case [e1_, Int() as e2_]:
                    return Multiply(e2_, e1_)
                case [e1_, e2_]:
                    return Multiply(e1_, e2_)

        case Let(x, e1, e2):
            e1_opt = recur(e1)
            match recur(e2):
                case Var(y) if y == x:
                    # If the body is just `x`, we can replace the entire Let with e1_opt
                    return e1_opt
                case body_opt:
                    return Let(x, e1_opt, body_opt)

        case Var():
            return expr

        case Bool():
            return expr

        case If(cond, then_, else_):
            c_opt = recur(cond)
            t_opt = recur(then_)
            e_opt = recur(else_)

            match c_opt:
                case Bool(True):
                    return t_opt
                case Bool(False):
                    return e_opt
                case _:
                    return If(c_opt, t_opt, e_opt)

        case LessThan(e1, e2):
            left = recur(e1)
            right = recur(e2)
            if isinstance(left, Int) and isinstance(right, Int):
                return Bool(left.value < right.value)
            else:
                return LessThan(left, right)

        case EqualTo(e1, e2):
            left = recur(e1)
            right = recur(e2)
            if isinstance(left, Int) and isinstance(right, Int):
                return Bool(left.value == right.value)
            elif isinstance(left, Bool) and isinstance(right, Bool):
                return Bool(left.value == right.value)
            else:
                return EqualTo(left, right)

        case GreaterThanOrEqualTo(e1, e2):
            left = recur(e1)
            right = recur(e2)
            if isinstance(left, Int) and isinstance(right, Int):
                return Bool(left.value >= right.value)
            else:
                return GreaterThanOrEqualTo(left, right)

        case Cell(value):
            return Cell(recur(value))

        case Get(cell):
            # ADDED: If the `cell` is itself literally `Cell(...)` after recursion,
            # we can replace `Get(Cell(...))` with that Cell’s value.
            new_cell = recur(cell)
            if isinstance(new_cell, Cell):
                return new_cell.value
            else:
                return Get(new_cell)

        case Set(cell, value):
            return Set(recur(cell), recur(value))

        case Do(effect, value):
            return Do(recur(effect), recur(value))

        case While(condition, body):
            c_opt = recur(condition)
            b_opt = recur(body)
            if isinstance(c_opt, Bool) and not c_opt.value:
                return Unit()
            else:
                return While(c_opt, b_opt)

        case _:
            raise NotImplementedError()
