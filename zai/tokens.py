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

from enum import Enum, auto


class TokType(Enum):
    """ Class representing all token types generated by the lexer. """

    # Atom types
    STRING = auto()
    ID = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()

    COMMA = auto()
    # A semicolon ";"
    SEMIC = auto()
    # Single quote '
    QUOTE = auto()
    # Double quote "
    DQUOTE = auto()
    LROUND = auto()
    RROUND = auto()
    LSQUARE = auto()
    RSQUARE = auto()
    LCURLY = auto()
    RCURLY = auto()
    # Comparison op
    EQ = auto()
    NEQ = auto
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()

    # arith op
    PLUS = auto()
    MINUS = auto()
    DIV = auto()
    MUL = auto()
    INCR = auto()
    DECR = auto()

    # Boolean op
    BANG = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()

    # Control flow
    IF = auto()
    ELSE = auto()
    ELIF = auto()
    WHILE = auto()
    FOR = auto()
    SWITCH = auto()
    CASE = auto()
    DO = auto()
    DEFAULT = auto()
    BREAK = auto()
    CONTINUE = auto()

    # Variable Assignment
    ASSIGN = auto()
    ADDASSIGN = auto()
    SUBASSIGN = auto()
    LET = auto()

    # MISC.
    FUNC = auto()
    CLASS = auto()
    DOT = auto()
    THIS = auto()
    PRINT = auto()
    RETURN = auto()
    NIL = auto()
    IMPORT = auto()
    AS = auto()
    EOF = auto()

    def __str__(self):
        tok_type_to_str = {
            "STRING": "string",
            "ID": "identifier",
            "BOOL": "boolean",
            "INT": "integer",
            "FLOAT": "float",
            "COMMA": ",",
            "SEMIC": ";",
            "COLON": ":",
            "QUOTE": "'",
            "DQUOTE": '"',
            "LROUND": "(",
            "RROUND": ")",
            "LSQUARE": "[",
            "RSQUARE": "]",
            "LCURLY": "{",
            "RCURLY": "}",
            "EQ": "==",
            "NEQ": "!=",
            "LT": "<",
            "GT": ">",
            "LTE": "<=",
            "GTE": ">",
            "PLUS": "+",
            "MINUS": "-",
            "DIV": "/",
            "MUL": "*",
            "INCR": "++",
            "DECR": "--",
            "BANG": "!",
            "TRUE": "true",
            "FALSE": "false",
            "AND": "&&",
            "OR": "||",
            "IF": "if keyword",
            "ELSE": "else keyword",
            "ELIF": "elif keyword",
            "WHILE": "while keyword",
            "FOR": "for keyword",
            "SWITCH": "switch keyword",
            "CASE": "case keyword",
            "DO": "do keyword",
            "DEFAULT": "default keyword",
            "BREAK": "break keyword",
            "CONTINUE": "continue keyword",
            "ASSIGN": "=",
            "ADDASSIGN": "+=",
            "SUBASSIGN": "-=",
            "LET": "let keyword",
            "FUNC": "func keyword",
            "CLASS": "class keyword",
            "DOT": ".",
            "THIS": "this keyword",
            "PRINT": "print keyword",
            "RETURN": "return keyword",
            "NIL": "nil",
            "IMPORT": "import keyword",
            "AS": "as keyword",
            "EOF": "End Of File Marker",
        }
        return tok_type_to_str[self.name]


class Token:
    """Token class used for all tokens generated by the lexer."""

    def __init__(self, tok_type, lexeme=None, line_num=None, col_num=None):
        """Generate a new token.

        Args:
            tok_type : The type of token.
            lexeme : Lexeme stored by the token. Defaults to None.
            line_num : Line number where lexeme was encountered.. Defaults to None.
            col_num : Column number where lexeme starts. Defaults to None.
        """
        self.tok_type = tok_type
        self.lexeme = lexeme
        self.line_num = line_num
        self.col_num = col_num

    def __str__(self):
        if self.lexeme is not None:
            return "(T:{} Le:{} C:{} L:{})".format(self.tok_type, self.lexeme, self.col_num, self.line_num)
        else:
            return "(T:{} C:{} L:{})".format(self.tok_type, self.col_num, self.line_num)

    def __repr__(self):
        if self.lexeme is not None:
            return "(T:{} Le:{} C:{} L:{})".format(self.tok_type, self.lexeme, self.col_num, self.line_num)
        else:
            return "(T:{} C:{} L:{})".format(self.tok_type, self.col_num, self.line_num)

    def __eq__(self, right):
        # Necessary to compare TokType with a token.
        if isinstance(right, Enum):
            if right == self.tok_type:
                return True
            else:
                return False
        elif self.tok_type == right.tok_type and self.lexeme == right.lexeme:
            return True

        return False


# Dictionary containing words reserved by language and their corresponding tokens
keywords = {
    "if": TokType.IF,
    "else": TokType.ELSE,
    "elif": TokType.ELIF,
    "while": TokType.WHILE,
    "for": TokType.FOR,
    "print": TokType.PRINT,
    "true": TokType.TRUE,
    "false": TokType.FALSE,
    "let": TokType.LET,
    "func": TokType.FUNC,
    "and": TokType.AND,
    "or": TokType.OR,
    "switch": TokType.SWITCH,
    "case": TokType.CASE,
    "default": TokType.DEFAULT,
    "class": TokType.CLASS,
    # "this": TokType.THIS,
    "return": TokType.RETURN,
    "break": TokType.BREAK,
    "continue": TokType.CONTINUE,
    "do": TokType.DO,
    "nil": TokType.NIL,
    "import": TokType.IMPORT,
    "as": TokType.AS,
}
