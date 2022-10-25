#!/usr/bin/env python3

import argparse
import sys

from typing import List
from hooks.commands import FormattingCommand
from hooks.error import CommandError

parser = argparse.ArgumentParser(
        description="Check C/C++ source files' formatting against "
                    "the current project clang-format configuration."
    )

parser.add_argument('--apply-fixes', action=argparse.BooleanOptionalAction,
                    dest='fix', help='Apply fixes whenever possible')

parser.add_argument('--verbose', action=argparse.BooleanOptionalAction,
                    dest='verbose', help='Show clang-format output')

parser.add_argument('files', metavar='File', nargs='+',
                    help='The files to check against the configuration')


class ClangFormat(FormattingCommand):
    def __init__(self) -> None:
        super().__init__("clang-format", parser)
        self.require_diff(True)

    def parse_args(self, args: List[str]) -> None:
        super().parse_args(args)
        if self.args.fix:
            self.apply_fixes('-i')
        self.set_verbose(self.args.verbose)

    def __call__(self) -> bool:
        if self.args is None:
            CommandError.InvalidOperation(self.command,
                                          "Args not parsed before execution")
        args = ["--style=file"]
        return super().__call__(self.args.files, args)


def main(argv: List[str] = sys.argv) -> bool:
    clang_format = ClangFormat()
    clang_format.parse_args(argv[1:])
    return clang_format()


if __name__ == "__main__":
    if not main():
        sys.exit(1)
