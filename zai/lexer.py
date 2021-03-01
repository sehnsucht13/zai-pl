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

"""
Module containing lexer class used to convert an input string into a sequence
of language tokens.
"""
from zai.tokens import Tok_Type, Token, keywords
from zai.internal_error import InternalTokenErr


class Lexer:
    """Class used to convert a string of characters into language tokens."""

    def __init__(self):
        self.text = None
        self.token_stream = list()
        # Current char observed
        self.curr_char = None
        # Current index within the input stream
        self.curr_idx = -1
        # Total length of input stream
        self.input_len = 0

        self.curr_lin_num = 0
        self.curr_col_num = 0

        # Special characters which are restricted/permitted in ID tokens.
        self.restricted_ident_chars = ".,:;()|&[]*/+-<=>!{}#\"'\n\t "
        self.permitted_ident_chars = "?@$"

    def _advance(self):
        """Advance the current character by one and return it. If there is no next character,
        return None."""
        if self.curr_idx + 1 < self.input_len:
            self.curr_idx += 1
            self.curr_char = self.text[self.curr_idx]
            self.curr_col_num += 1
            return self.curr_char
        else:
            self.curr_char = None
            return None

    def _peek(self):
        """Return the next character in the input text sequence. If there is no next
        character, return None."""
        if self.curr_idx + 1 < self.input_len:
            return self.text[self.curr_idx + 1]
        else:
            return None

    def _tokenize_ident(self):
        """ Tokenize an identifier and return its lexeme."""
        ident_str = str(self.curr_char)
        # ident_str += self.curr_char
        while (
            self._peek() is not None and self._peek() not in self.restricted_ident_chars
        ):
            self._advance()
            ident_str += self.curr_char
        return ident_str

    def _tokenize_num(self):
        """ Tokenize a single integer number and return it in integer form."""
        num_str = str()
        num_str += self.curr_char
        while self._peek() is not None and self._peek() in "1234567890":
            self._advance()
            num_str += self.curr_char
        return num_str

    def _tokenize_str(self):
        str_content = str()
        while True:
            if self.curr_char is None:
                self.token_stream.append(
                    Token(
                        Tok_Type.STRING,
                        str_content,
                        self.curr_lin_num,
                        self.curr_col_num,
                    )
                )
                return
            elif self.curr_char != "\\" and self._peek() == '"':
                str_content += self.curr_char
                self.token_stream.append(
                    Token(
                        Tok_Type.STRING,
                        str_content,
                        self.curr_lin_num,
                        self.curr_col_num,
                    )
                )
                self._advance()
                self.token_stream.append(
                    Token(Tok_Type.DQUOTE, None, self.curr_lin_num, self.curr_col_num)
                )
                return
            else:
                str_content += self.curr_char
                self._advance()

    def _tokenize(self):
        """ Tokenize the current text sequence and return the tokens generated. """
        while self._advance() is not None:
            if self.curr_char == "\n":
                # Increment line numbers
                self.curr_lin_num += 1
                # Reset current column number
                self.curr_col_num = 0
            elif self.curr_char == "(":
                self.token_stream.append(
                    Token(Tok_Type.LROUND, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ")":
                self.token_stream.append(
                    Token(Tok_Type.RROUND, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ".":
                self.token_stream.append(
                    Token(Tok_Type.DOT, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ",":
                self.token_stream.append(
                    Token(Tok_Type.COMMA, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ":":
                self.token_stream.append(
                    Token(Tok_Type.COLON, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == ";":
                self.token_stream.append(
                    Token(Tok_Type.SEMIC, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "{":
                self.token_stream.append(
                    Token(Tok_Type.LCURLY, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "}":
                self.token_stream.append(
                    Token(Tok_Type.RCURLY, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "[":
                self.token_stream.append(
                    Token(Tok_Type.LSQUARE, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "]":
                self.token_stream.append(
                    Token(Tok_Type.RSQUARE, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "-":
                if self._peek() == "-":
                    self.token_stream.append(
                        Token(Tok_Type.DECR, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                elif self._peek() == "=":
                    self.token_stream.append(
                        Token(
                            Tok_Type.SUBASSIGN,
                            None,
                            self.curr_lin_num,
                            self.curr_col_num,
                        )
                    )
                    self._advance()
                else:
                    self.token_stream.append(
                        Token(
                            Tok_Type.MINUS, None, self.curr_lin_num, self.curr_col_num
                        )
                    )
            elif self.curr_char == "&":
                if self._peek() == "&":
                    self.token_stream.append(
                        Token(Tok_Type.AND, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                else:
                    raise InternalTokenErr(
                        self.curr_lin_num,
                        self.curr_col_num,
                        self.text,
                        (
                            "A single '&' is not a valid symbol or operator. Did you"
                            "mean to use '&&'(AND) operator?"
                        ),
                    )
            elif self.curr_char == "|":
                if self._peek() == "|":
                    self.token_stream.append(
                        Token(Tok_Type.OR, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                else:
                    raise InternalTokenErr(
                        self.curr_lin_num,
                        self.curr_col_num,
                        self.text,
                        (
                            "A single '|' is not a valid symbol or operator. Did you "
                            "mean to use '||'(OR) operator?"
                        ),
                    )
            elif self.curr_char == "+":
                if self._peek() == "+":
                    self.token_stream.append(
                        Token(Tok_Type.INCR, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                elif self._peek() == "=":
                    self.token_stream.append(
                        Token(
                            Tok_Type.ADDASSIGN,
                            None,
                            self.curr_lin_num,
                            self.curr_col_num,
                        )
                    )
                    self._advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.PLUS, None, self.curr_lin_num, self.curr_col_num)
                    )
            elif self.curr_char == "/":
                self.token_stream.append(
                    Token(Tok_Type.DIV, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "*":
                self.token_stream.append(
                    Token(Tok_Type.MUL, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == '"':
                self.token_stream.append(
                    Token(Tok_Type.DQUOTE, None, self.curr_lin_num, self.curr_col_num)
                )
                # Skip over the current character which is a double quote
                self._advance()
                self._tokenize_str()
            elif self.curr_char == "'":
                self.token_stream.append(
                    Token(Tok_Type.QUOTE, None, self.curr_lin_num, self.curr_col_num)
                )
            elif self.curr_char == "!":
                if self._peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.NEQ, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.BANG, None, self.curr_lin_num, self.curr_col_num)
                    )
            elif self.curr_char == "=":
                if self._peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.EQ, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                else:
                    self.token_stream.append(
                        Token(
                            Tok_Type.ASSIGN, None, self.curr_lin_num, self.curr_col_num
                        )
                    )
            elif self.curr_char == "<":
                if self._peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.LTE, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.LT, None, self.curr_lin_num, self.curr_col_num)
                    )
            elif self.curr_char == ">":
                if self._peek() == "=":
                    self.token_stream.append(
                        Token(Tok_Type.GTE, None, self.curr_lin_num, self.curr_col_num)
                    )
                    self._advance()
                else:
                    self.token_stream.append(
                        Token(Tok_Type.GT, None, self.curr_lin_num, self.curr_col_num)
                    )
            elif (
                self.curr_char in self.permitted_ident_chars or self.curr_char.isalpha()
            ):
                # Store the column at the start of the identifier
                ident_start_col = self.curr_col_num
                ident = self._tokenize_ident()

                # Check if the current identifier is a keyword.
                token = keywords.get(ident, None)
                if token is None:
                    token = Token(
                        Tok_Type.ID, ident, self.curr_lin_num, ident_start_col
                    )
                else:
                    token = Token(token, None, self.curr_lin_num, ident_start_col)

                self.token_stream.append(token)
            elif self.curr_char.isdigit():
                # Store the column at the start of the number
                num_start_col = self.curr_col_num
                num_str = self._tokenize_num()

                # Check if the number being tokenized might actually be a bad identifier
                # which starts with a number.
                # Example: 13abc or 1Alph@
                if self._peek() is not None and (
                    self._peek() == self.permitted_ident_chars or self._peek().isalpha()
                ):
                    raise InternalTokenErr(
                        self.curr_lin_num,
                        num_start_col,
                        self.text,
                        "Identifiers cannot start with integers!",
                    )
                self.token_stream.append(
                    Token(Tok_Type.NUM, int(num_str), self.curr_lin_num, num_start_col)
                )

        # Add final EOF token to indicate end of token stream
        self.token_stream.append(
            Token(Tok_Type.EOF, None, self.curr_lin_num, self.curr_col_num)
        )

    def _reset_internal_state(self):
        """Reset the internal state of the lexer for a new input string."""
        self.input_len = len(self.text)

        # Reset all other variables
        self.token_stream = list()
        self.curr_char = None
        self.curr_idx = -1
        self.curr_lin_num = 0
        self.curr_col_num = 0

    def tokenize_string(self, input_str):
        """ Tokenize a single input string. Returns the token stream produced."""
        if self.text is not None:
            self.text = input_str
            self._reset_internal_state()
        else:
            self.text = input_str
            self.input_len = len(input_str)

        if self.input_len > 0:
            self._tokenize()
            return self.token_stream
        else:
            return [Token(Tok_Type.EOF)]
