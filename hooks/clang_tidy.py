#!/usr/bin/env python3

import argparse
import sys

from typing import List
from hooks.commands import SyntaxAnalyzer
from hooks.error import CommandError

parser = argparse.ArgumentParser(
        description="Check C/C++ source files' syntax against "
                    "the current project clang-tidy configuration."
    )

parser.add_argument('--apply-fixes', action=argparse.BooleanOptionalAction,
                    dest='fix', help='Apply fixes whenever possible')

parser.add_argument('--verbose', action=argparse.BooleanOptionalAction,
                    dest='verbose', help='Show clang-format output')

parser.add_argument('files', metavar='File', nargs='+',
                    help='The files to check against the configuration')


class ClangTidy(SyntaxAnalyzer):
    def __init__(self) -> None:
        super().__init__("clang-tidy", parser)

    def parse_args(self, args: List[str]) -> None:
        super().parse_args(args)
        if self.args.fix:
            self.apply_fixes('--fix-errors')
        self.set_verbose(self.args.verbose)

    def __call__(self) -> bool:
        if self.args is None:
            CommandError.InvalidOperation(self.command,
                                          "Args not parsed before execution")
        args = ["--quiet"]
        return super().__call__(self.args.files, args)


def main(argv: List[str] = sys.argv) -> bool:
    clang_tidy = ClangTidy()
    clang_tidy.check_installed()
    clang_tidy.parse_args(argv[1:])
    return clang_tidy()


if __name__ == "__main__":
    sys.exit(main())
