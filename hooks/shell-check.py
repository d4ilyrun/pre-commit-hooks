#!/usr/bin/env python3

import argparse
import sys

from typing import List
from commands import SyntaxAnalyzer
from error import CommandError

parser = argparse.ArgumentParser(
        description="Check the syntax of shell scripts"
    )

parser.add_argument('--verbose', action=argparse.BooleanOptionalAction,
                    dest='verbose', help='Show clang-format output')

parser.add_argument('files', metavar='File', nargs='+',
                    help='The files to check against the configuration')

# TODO: Pass shellcheck arguments


class ShellCheck(SyntaxAnalyzer):
    def __init__(self) -> None:
        super().__init__("shellcheck", parser)

    def parse_args(self, args: List[str]) -> None:
        super().parse_args(args)
        self.set_verbose(self.args.verbose)

    def __call__(self) -> bool:
        if self.args is None:
            CommandError.InvalidOperation(self.command,
                                          "Args not parsed before execution")
        args = []
        return super().__call__(self.args.files, args)


def main(argv: List[str] = sys.argv) -> bool:
    shell_check = ShellCheck()
    shell_check.check_installed()
    shell_check.parse_args(argv[1:])
    return shell_check()


if __name__ == "__main__":
    if not main():
        sys.exit(1)
