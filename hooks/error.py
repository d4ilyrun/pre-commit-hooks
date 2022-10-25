#!/usr/bin/env python3

import sys


class Error:
    """ Super class for all errors """
    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg

    def show(self) -> None:
        sys.stderr.write(">> {} [code: {}]\n".format(self.msg, self.code))

    def throw(self) -> None:
        self.show()
        sys.exit(self.code)


class CommandError(Error):
    """ Class for creating command related errors """
    def __init__(self, code: int, command: str, msg: str) -> None:
        self.command = command
        self.details = Error(code, msg)

    # TODO: Add colors
    def throw(self):
        """ Output an error to STDERR and exit with the corresponding code """
        sys.stderr.write("Error with {}:\n".format(self.command))
        self.details.throw()

    @staticmethod
    def NotFound(command: str) -> None:
        CommandError(127, command, "Command not found").throw()

    @staticmethod
    def InvalidOperation(command: str, details: str) -> None:
        CommandError(1, command, "Error during execution: " + details).throw()
