from kernel import Program, Int, Unary, Binary, Let, Var, Bool, If, Unit, While
from remove_complex_operands import remove_complex_operands
from explicate_control import explicate_control
from util import SequentialNameGenerator


def main() -> None:
    program = Program(
        [],
        Let(
            "x",
            Unary("cell", Int(0)),
            While(
                Binary("<", Unary("^", Var("x")), Int(5)),
                Binary(
                    ":=",
                    Var("x"),
                    Binary("+", Unary("^", Var("x")), Int(1)),
                ),
            ),
        ),
    )

    fresh = SequentialNameGenerator()
    result = remove_complex_operands(program, fresh)
    result = explicate_control(result, fresh)
    print(result)


if __name__ == "__main__":
    main()
