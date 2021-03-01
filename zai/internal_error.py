# Copyright 2021 by Yavor Konstantinov <ykonstantinov1@gmail.com>

# This file is part of zai-pl.

# zai-pl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# zai-pl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with zai-pl. If not, see <https://www.gnu.org/licenses/>.

""" Module contains error classes used to transfer control and signal errors
encountered during execution."""


class InternalErr(Exception):
    """
    Base class for all internal errors used by the interpreter.
    """

    def __init__(
        self,
    ):
        raise NotImplementedError()


class InternalTypeError(InternalErr):
    def __init__(self, operation, left_type, right_type=None):
        """Class representing an internal error encountered during and basic operations
        between one or more types.
        """
        self.operation = operation
        self.left = left_type
        self.right = right_type
        self.err_msg = str()

        if self.right is None:
            self.err_msg = "The operation {} is not allowed on a {}!".format(
                self.operation, str(self.left)
            )
        else:
            self.err_msg = (
                "The operation {} is not allowed between a {} and a {}!".format(
                    self.operation, str(self.left), str(self.right)
                )
            )

    def __str__(self):
        return "Typecheck Error: {}".format(self.err_msg)

    def __repr__(self):
        "Internal Runtime Error: Operation {}, Left Side: {}, Right Side: {}".format(
            self.operation, self.left, self.right
        )


class InternalRuntimeErr(InternalErr):
    """
    Class representing an internal error encountered during runtime.
    """

    def __init__(self, message):
        "Class representing internal errors encountered during runtime."
        self.message = message

    def __str__(self):
        return "Runtime Error: {}".format(self.message)

    def __repr__(self):
        "Internal Runtime Error: {}".format(self.message)


class InternalParseErr(InternalErr):
    """
    Class representing an internal error encountered during parsing/lexing stages.
    """

    def __init__(
        self,
        line_num,
        col_num,
        original_text,
        expected_tokens,
        got_token,
    ):
        "Class representing internal errors encountered during parsing/lexing stage."
        self.line_num = line_num
        self.col_num = col_num
        self.source_text_lines = original_text.split("\n")
        self.got_token = got_token
        self.expected_tokens = expected_tokens

        wanted_tokens = ""
        if isinstance(self.expected_tokens, list):
            for tok in self.expected_tokens:
                wanted_tokens += str(tok)
        else:
            wanted_tokens = str(self.expected_tokens)

        self.err_msg = "Expected a '{}' token but received '{}'".format(
            wanted_tokens, self.got_token
        )

    def __str__(self):
        return "Parse Error: Line: {}, Column: {}\n\n  {}\n\nExplanation: {}".format(
            self.line_num,
            self.col_num,
            self.source_text_lines[self.line_num],
            self.err_msg,
        )

    def __repr__(self):
        return (
            "Internal Parse Error: Line: {}, Column: {}\n\n  {}\n\n" "Explanation: {}"
        ).format(
            self.line_num,
            self.col_num,
            self.source_text_lines[self.line_num],
            self.err_msg,
        )


class InternalTokenErr(InternalErr):
    """
    Class representing an internal error encountered during lexing stages.
    """

    def __init__(self, line_num, col_num, original_text, err_details):
        "Class representing internal errors encountered during lexing stage."
        self.line_num = line_num
        self.col_num = col_num
        self.text = original_text.split("\n")
        self.err_details = err_details
        print("error line", self.text[self.line_num])

    def __str__(self):
        return "Token Error: Error on line {}, column {}\n  {}\n{}\n{}".format(
            self.line_num,
            self.col_num,
            self.text[self.line_num],
            "      _".rjust(self.col_num - 1, " "),
            self.err_details,
        )

    def __repr__(self):
        return "Internal Token Error: Error on line {}, column {}\n  {}".format(
            self.line_num, self.col_num, self.text[self.line_num]
        )
