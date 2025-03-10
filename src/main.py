from llvmlite.ir import Module  # type: ignore
from llvmlite.binding import parse_assembly, ModuleRef, PipelineTuningOptions  # type: ignore
from parse import parse
from simplify import simplify
from assignment_conversion import convert_assignments
from uniqify import uniqify
from opt import opt
from explicate_control import explicate_control
from close_lambdas import close
from hoist import hoist
from lower import lower

from util import SequentialNameGenerator


def compile(source: str) -> Module:
    fresh = SequentialNameGenerator()
    program = parse(source)
    program = simplify(program, fresh)
    program = convert_assignments(program)
    program = uniqify(program, fresh)
    program = opt(program)
    program = explicate_control(program, fresh)
    program = close(program, fresh)
    program = hoist(program, fresh)
    return lower(program)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="471c")
    parser.add_argument("input", type=argparse.FileType("r"))
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), default="-")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--args", default=[], action="extend", nargs="*", type=str, help="")
    options = parser.parse_args()

    with options.input as input:
        module = compile(input.read())

        print(module, file=options.output)

        if options.run:
            from execute import execute

            result = execute(str(module), options.args)
            print(result)
