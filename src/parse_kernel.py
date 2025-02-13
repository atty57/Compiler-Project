import os
from typing import Literal
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
    Bool,
    If,
    Compare,
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
        x: Expression,
        y: Expression,
    ) -> Add:
        return Add(x, y)

    def subtract_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> Subtract:
        return Subtract(x, y)

    def multiply_expr(
        self,
        x: Expression,
        y: Expression,
    ) -> Multiply:
        return Multiply(x, y)

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

    def bool_expr(
        self,
        value: bool,
    ) -> Bool:
        return Bool(value)

    def if_expr(
        self,
        condition: Expression,
        consequent: Expression,
        alternative: Expression,
    ) -> If:
        return If(condition, consequent, alternative)

    def compare_expr(
        self,
        operator: Literal["<", "==", ">="],
        e1: Expression,
        e2: Expression,
    ) -> Compare:
        return Compare(operator, e1, e2)

    def nat(
        self,
        value: Token,
    ) -> int:
        return int(value)

    def true(
        self,
        value: Token,
    ) -> bool:
        return True

    def false(
        self,
        value: Token,
    ) -> bool:
        return False

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
