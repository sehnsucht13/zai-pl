from enum import Enum, auto


class Tok_Type(Enum):
    """ Class representing all token types generated by the lexer. """

    # Atom types
    STRING = auto()
    ID = auto()
    BOOL = auto()
    NUM = auto()

    COMMA = auto()
    # A semicolon ";"
    SEMIC = auto()
    # A colon ":"
    COLON = auto()
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
    DEFAULT = auto()
    BREAK = auto()
    CONTINUE = auto()

    # Variable Assignment
    ASSIGN = auto()
    LET = auto()

    # MISC.
    FUNC = auto()
    CLASS = auto()
    DOT = auto()
    THIS = auto()
    PRINT = auto()
    RETURN = auto()
    EOF = auto()


class Token:
    """Token class used for all tokens generated by the lexer.
    """

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
            return "(T:{} Le:{} C:{} L:{})".format(
                self.tok_type, self.lexeme, self.col_num, self.line_num
            )
        else:
            return "(T:{} C:{} L:{})".format(self.tok_type, self.col_num, self.line_num)

    def __repr__(self):
        if self.lexeme is not None:
            return "(T:{} Le:{} C:{} L:{})".format(
                self.tok_type, self.lexeme, self.col_num, self.line_num
            )
        else:
            return "(T:{} C:{} L:{})".format(self.tok_type, self.col_num, self.line_num)

    def __eq__(self, right):
        # Necessary to compare Tok_Type with a token.
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
    "if": Token(Tok_Type.IF),
    "else": Token(Tok_Type.ELSE),
    "elif": Token(Tok_Type.ELIF),
    "while": Token(Tok_Type.WHILE),
    "for": Token(Tok_Type.FOR),
    "print": Token(Tok_Type.PRINT),
    "true": Token(Tok_Type.TRUE),
    "false": Token(Tok_Type.FALSE),
    "let": Token(Tok_Type.LET),
    "func": Token(Tok_Type.FUNC),
    "and": Token(Tok_Type.AND),
    "or": Token(Tok_Type.OR),
    "switch": Token(Tok_Type.SWITCH),
    "case": Token(Tok_Type.CASE),
    "default": Token(Tok_Type.DEFAULT),
    "class": Token(Tok_Type.CLASS),
    "this": Token(Tok_Type.THIS),
    "return": Token(Tok_Type.RETURN),
    "break": Token(Tok_Type.BREAK),
    "continue": Token(Tok_Type.CONTINUE),
}
