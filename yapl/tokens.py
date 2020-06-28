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

    FUNC = auto()
    ASSIGN = auto()
    IF = auto()
    WHILE = auto()
    FOR = auto()
    PRINT = auto()
    LET = auto()
    ELSE = auto()
    EOF = auto()


class Token:
    def __init__(self, tok_type, literal=None, line_num=None, col_num=None):
        self.tok_type = tok_type
        self.literal = literal
        self.line_num = line_num
        self.col_num = col_num

    def __str__(self):
        if self.literal is not None:
            return "({} {})".format(self.tok_type, self.literal)
        else:
            return "({})".format(self.tok_type)

    def __repr__(self):
        if self.literal is not None:
            return "({} {})".format(self.tok_type, self.literal)
        else:
            return "({})".format(self.tok_type)

    def __eq__(self, right):
        if self.tok_type == right.tok_type and self.literal == right.literal:
            return True
        return False


# Dictionary containing words reserved by language and their corresponding tokens
keywords = {
    "if": Token(Tok_Type.IF),
    "while": Token(Tok_Type.WHILE),
    "for": Token(Tok_Type.FOR),
    "print": Token(Tok_Type.PRINT),
    "else": Token(Tok_Type.ELSE),
    "true": Token(Tok_Type.TRUE),
    "false": Token(Tok_Type.FALSE),
    "let": Token(Tok_Type.LET),
    "func": Token(Tok_Type.FUNC),
    "and": Token(Tok_Type.AND),
    "or": Token(Tok_Type.OR),
}
