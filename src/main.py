from llvmlite import ir  # type: ignore
from parse_kernel import parse
from uniqify import uniqify
from opt import opt
from remove_complex_operands import remove_complex_operands
from explicate_control import explicate_control
from lower import lower

from util import SequentialNameGenerator


def compile(source: str) -> ir.Module:
    program = parse(source)

    fresh = SequentialNameGenerator()
    result = uniqify(program, fresh)
    result = opt(result)
    result = remove_complex_operands(result, fresh)
    result = explicate_control(result, fresh)
    return lower(result)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="471c")
    parser.add_argument("input", type=argparse.FileType("r"), help="")
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default="-")
    parser.add_argument("--run", action="store_true", help="")
    parser.add_argument("--args", default=[], action="extend", nargs="*", type=str, help="")
    options = parser.parse_args()

    with options.input as input:
        module = compile(input.read())

        print(module, file=options.output)

        if options.run:
            from execute import execute

            result = execute(str(module), options.args)
            print(result)
