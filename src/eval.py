from collections.abc import Sequence, Mapping
from functools import partial
from kernel import Program, Expression, Int, Add, Subtract, Multiply, Let, Var

type Value = Int
type Environment = Mapping[str, Value]


def eval(
    program: Program,
    arguments: Sequence[Value],
) -> Value:
    env: Environment = {}
    return eval_expr(program.body, env)


def eval_expr(
    expr: Expression,
    env: Environment,
) -> Value:
    recur = partial(eval_expr, env=env)
    match expr:
        case Int():
            return expr

        case Add(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 + i2)

        case Subtract(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)

        case Multiply(e1, e2):
            match recur(e1), recur(e2):
                case [Int(i1), Int(i2)]:
                    return Int(i1 * i2)

        case Let(x, e1, e2):
            raise NotImplementedError()

        case Var(x):  # pragma: no branch
            raise NotImplementedError()
