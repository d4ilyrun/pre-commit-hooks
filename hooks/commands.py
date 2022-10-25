#!/usr/bin/env python3

import sys
import shutil
import subprocess as sp
from argparse import ArgumentParser
from typing import List

from hooks.error import Error, CommandError


class Command:
    """ Super class for all commands """
    def __init__(self, command: str, arg_parser: ArgumentParser) -> None:
        self.command = command
        self.arg_parser = arg_parser
        self.args = None
        self.verbose = False
        self.sucess = True

    def check_installed(self):
        """ Ensure that a command is installed """
        if shutil.which(self.command) is None:
            CommandError.NotFound(self.command)

    def parse_args(self, args: List[str]):
        """ Parse command arguments """
        if self.args is not None:
            return
        self.args = self.arg_parser.parse_args(args)

    def set_verbose(self, verbose: bool) -> None:
        self.verbose = verbose


class SyntaxAnalyzer(Command):
    """ Commands responsible for analyzing a syntax (clang-tidy, ...) """

    def __init__(self, command: str, arg_parser: ArgumentParser) -> None:
        super().__init__(command, arg_parser)
        self.fix = None

    def apply_fixes(self, flag: str):
        """ Wether to apply fixes whenever possible """
        self.fix = flag

    def __call__(self, files: List[str], args: List[str]) -> bool:
        """
            Run the command on the list of files with the given arguments.
            Return wether it was successful
        """
        # Add fix flag if set
        if self.fix:
            args.append(self.fix)
        # Check format for each file
        for file in files:
            cmd_args = [self.command, *args, file]
            if self.verbose:
                print("running: ", cmd_args)
            # Run analyze
            cmd = sp.run(cmd_args, stdout=sp.PIPE, stderr=sp.PIPE)
            if cmd.returncode != 0:
                Error(cmd.returncode, "{}: invalid syntax".format(file)).show()
                if self.verbose:
                    sys.stderr.write(cmd.stderr.decode('utf-8'))
                self.sucess = False
        return self.sucess


class FormattingCommand(Command):
    """ Commands responsible for formatting files """
    def __init__(self, command: str, arg_parser: ArgumentParser) -> None:
        super().__init__(command, arg_parser)
        self.fix = None
        self.diff = False

    def __call__(self, files: List[str], args: List[str]) -> bool:
        """
            Run the command on the list of files with the given arguments.
            Return wether it was successful
        """
        lines = ""
        # Add fix flag if set
        if self.fix:
            args.append(self.fix)
        # Check format for each file
        for file in files:
            cmd_args = [self.command, *args, file]
            if self.verbose:
                print("running: ", cmd_args)

            # Save file to compare later
            if self.diff:
                lines = self.__save_file(file)
            # Run formatting
            cmd = sp.run(cmd_args, stdout=sp.PIPE, stderr=sp.PIPE)
            # Compare the content before/after
            if self.diff and cmd.stdout.decode('ascii') != lines:
                cmd.returncode = 1
                cmd.stderr = '''
                    Output doesn't match the original content of the file\n
                '''.encode()

            if cmd.returncode != 0:
                Error(cmd.returncode, "{}: wrong format".format(file)).show()
                if self.verbose:
                    sys.stderr.write(cmd.stderr.decode('utf-8'))
                self.sucess = False
        return self.sucess

    def apply_fixes(self, flag: str):
        """ Wether to apply fixes whenever possible """
        self.fix = flag

    def require_diff(self, require: bool):
        """
            Wether we need to compare before/after formatting manually.
            Needed whend have no simple way of detecting errors otherwise.
            Example: clang-format
        """
        self.diff = require

    # PRIVATE FUNCTIONS

    def __save_file(self, file: str) -> str:
        """ Save the content of a file """
        with open(file) as f:
            return f.read()
