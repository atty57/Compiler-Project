import os
from lark import (
    Lark,
    ParseTree,
    Token,
    Transformer,
    v_args,  # type: ignore
)
from kernel import (
    Expression,
    Int,
    Add,
    Subtract,
    Multiply,
    Let,
    Var,
)


@v_args(inline=True)
class AstTransformer(Transformer[Token, Expression]):
    def int_expr(
        self,
        value: int,
    ) -> Int:
        return Int(value)

    def add_expr(
        self,
        e1: Expression,
        e2: Expression,
    ) -> Add:
        return Add(e1, e2)

    def subtract_expr(
        self,
        e1: Expression,
        e2: Expression,
    ) -> Subtract:
        return Subtract(e1, e2)

    def multiply_expr(
        self,
        e1: Expression,
        e2: Expression,
    ) -> Multiply:
        return Multiply(e1, e2)

    def let_expr(
        self,
        name: str,
        value: Expression,
        body: Expression,
    ) -> Let:
        return Let(name, value, body)

    def var_expr(
        self,
        name: str,
    ) -> Var:
        return Var(name)

    def nat(
        self,
        value: Token,
    ) -> int:
        return int(value)

    def identifier(
        self,
        value: Token,
    ) -> str:
        return str(value)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def parse_expr(
    source: str,
) -> Expression:
    with open(os.path.join(__location__, "./kernel.lark"), "r") as f:
        parser = Lark(f, start="expr")
        tree: ParseTree = parser.parse(source)
        return AstTransformer().transform(tree)  # type: ignore


if __name__ == "__main__":
    source = """
    (let ([x 1]) x)
    """
    expr = parse_expr(source)
    print(expr)
