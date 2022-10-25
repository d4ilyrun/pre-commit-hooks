#!/usr/bin/env python3

import argparse
import sys

from typing import List
from hooks.commands import FormattingCommand
from hooks.error import CommandError

parser = argparse.ArgumentParser(
        description="Check that Nix source files are formatted correctly"
    )

parser.add_argument('--apply-fixes', action=argparse.BooleanOptionalAction,
                    dest='fix', help='Apply fixes whenever possible')

parser.add_argument('--verbose', action=argparse.BooleanOptionalAction,
                    dest='verbose', help='Show clang-format output')

parser.add_argument('files', metavar='File', nargs='+',
                    help='The files to check against the configuration')


class NixpkgsFmt(FormattingCommand):
    def __init__(self) -> None:
        super().__init__("nixpkgs-fmt", parser)

    def parse_args(self, args: List[str]) -> None:
        super().parse_args(args)
        # Inversed as we can only tell nixpkgs to check
        if not self.args.fix:
            self.apply_fixes('--check')
        self.set_verbose(self.args.verbose)

    def __call__(self) -> bool:
        if self.args is None:
            CommandError.InvalidOperation(self.command,
                                          "Args not parsed before execution")
        return super().__call__(self.args.files, [])


def main(argv: List[str] = sys.argv) -> bool:
    nixpkgs_format = NixpkgsFmt()
    nixpkgs_format.check_installed()
    nixpkgs_format.parse_args(argv[1:])
    return nixpkgs_format()


if __name__ == "__main__":
    if not main():
        sys.exit(1)
