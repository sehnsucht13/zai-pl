from zai.lexer import Lexer
from zai.tokens import Tok_Type, Token
from zai.internal_error import InternalTokenErr
import pytest


def compare_tokens(l1, l2):
    """
    Compare two token lists token by token. Return True if all elements are equal.
    Return False if there is any mismatch.
    """
    # Check length of both lists
    len_l1 = len(l1)
    len_l2 = len(l2)
    assert len_l1 == len_l2, "Token stream length is not equal!"

    # Compare element by element
    # The __eq__ method of the token class is overriden and a deep comparison
    # of the two tokens is done there
    for idx, token in enumerate(l1):
        assert token == l2[idx], "Tokens are not equal"


def test_newline():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("\n")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("\r\n")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)


def test_empty_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)


def test_whitespace_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string(" ")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)

    # 1 TAB
    lexer_output = lexer.tokenize_string("  ")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)

    # 2 TABS
    lexer_output = lexer.tokenize_string("          ")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)


def test_comments():
    lexer = Lexer()

    lexer_output = lexer.tokenize_string("//")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("// // 4 + 4")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("// A comment")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("abc // A comment")
    expected = [Token(Tok_Type.ID, "abc"), Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)


def test_special_chars():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("(),;{}[]-+/*'! != = == < <= > >=")
    expected = [
        Token(Tok_Type.LROUND),
        Token(Tok_Type.RROUND),
        Token(Tok_Type.COMMA),
        Token(Tok_Type.SEMIC),
        Token(Tok_Type.LCURLY),
        Token(Tok_Type.RCURLY),
        Token(Tok_Type.LSQUARE),
        Token(Tok_Type.RSQUARE),
        Token(Tok_Type.MINUS),
        Token(Tok_Type.PLUS),
        Token(Tok_Type.DIV),
        Token(Tok_Type.MUL),
        Token(Tok_Type.QUOTE),
        Token(Tok_Type.BANG),
        Token(Tok_Type.NEQ),
        Token(Tok_Type.ASSIGN),
        Token(Tok_Type.EQ),
        Token(Tok_Type.LT),
        Token(Tok_Type.LTE),
        Token(Tok_Type.GT),
        Token(Tok_Type.GTE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


# Symbols without special chars
def test_symbol_lex_no_special():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("h")
    expected = [
        Token(Tok_Type.ID, "h"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("hello")
    expected = [
        Token(Tok_Type.ID, "hello"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("helloWorld")
    expected = [
        Token(Tok_Type.ID, "helloWorld"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("MixEDCase")
    expected = [
        Token(Tok_Type.ID, "MixEDCase"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("symOne symTwo")
    expected = [
        Token(Tok_Type.ID, "symOne"),
        Token(Tok_Type.ID, "symTwo"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_symbol_lex_special():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("$")
    expected = [
        Token(Tok_Type.ID, "$"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("@")
    expected = [
        Token(Tok_Type.ID, "@"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("?")
    expected = [
        Token(Tok_Type.ID, "?"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("hello@worl$d?")
    expected = [
        Token(Tok_Type.ID, "hello@worl$d?"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("hello@worl$d?123")
    expected = [
        Token(Tok_Type.ID, "hello@worl$d?123"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("h3llo@worl$d")
    expected = [
        Token(Tok_Type.ID, "h3llo@worl$d"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("Symb0lOn3? Symb0lTw0?")
    expected = [
        Token(Tok_Type.ID, "Symb0lOn3?"),
        Token(Tok_Type.ID, "Symb0lTw0?"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("one_two")
    expected = [
        Token(Tok_Type.ID, "one_two"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("Symb0lOn3? Symb0lTw0?_three")
    expected = [
        Token(Tok_Type.ID, "Symb0lOn3?"),
        Token(Tok_Type.ID, "Symb0lTw0?_three"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_symbols_mixed_with_numbers():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("mixed_4_sym")
    expected = [
        Token(Tok_Type.ID, "mixed_4_sym"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("@43abc")
    expected = [
        Token(Tok_Type.ID, "@43abc"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("@a4_33$3")
    expected = [
        Token(Tok_Type.ID, "@a4_33$3"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_number_lex():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("1")
    expected = [
        Token(Tok_Type.NUM, 1),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("0")
    expected = [
        Token(Tok_Type.NUM, 0),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("233")
    expected = [
        Token(Tok_Type.NUM, 233),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("233 455")
    expected = [
        Token(Tok_Type.NUM, 233),
        Token(Tok_Type.NUM, 455),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("-233")
    expected = [
        Token(Tok_Type.MINUS),
        Token(Tok_Type.NUM, 233),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string('"hello world"')
    expected = [
        Token(Tok_Type.DQUOTE, None),
        Token(Tok_Type.STRING, "hello world"),
        Token(Tok_Type.DQUOTE, None),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string('"1 number with another number 2"')
    expected = [
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.STRING, "1 number with another number 2"),
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_language_keywords():
    lexer = Lexer()

    lexer_output = lexer.tokenize_string("if")
    expected = [
        Token(Tok_Type.IF),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("while")
    expected = [
        Token(Tok_Type.WHILE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("for")
    expected = [
        Token(Tok_Type.FOR),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("print")
    expected = [
        Token(Tok_Type.PRINT),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("else")
    expected = [
        Token(Tok_Type.ELSE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("true")
    expected = [
        Token(Tok_Type.TRUE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("false")
    expected = [
        Token(Tok_Type.FALSE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("func")
    expected = [
        Token(Tok_Type.FUNC),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("switch")
    expected = [
        Token(Tok_Type.SWITCH),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("case")
    expected = [
        Token(Tok_Type.CASE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("default")
    expected = [
        Token(Tok_Type.DEFAULT),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("import")
    expected = [
        Token(Tok_Type.IMPORT),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("as")
    expected = [
        Token(Tok_Type.AS),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("do")
    expected = [
        Token(Tok_Type.DO),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("return")
    expected = [
        Token(Tok_Type.RETURN),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("continue")
    expected = [
        Token(Tok_Type.CONTINUE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("break")
    expected = [
        Token(Tok_Type.BREAK),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("nil")
    expected = [
        Token(Tok_Type.NIL),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("this")
    expected = [
        Token(Tok_Type.THIS),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("or")
    expected = [
        Token(Tok_Type.OR),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("and")
    expected = [
        Token(Tok_Type.AND),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("+=")
    expected = [
        Token(Tok_Type.ADDASSIGN),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("-=")
    expected = [
        Token(Tok_Type.SUBASSIGN),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("++")
    expected = [
        Token(Tok_Type.INCR),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("--")
    expected = [
        Token(Tok_Type.DECR),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("&&")
    expected = [
        Token(Tok_Type.AND),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("||")
    expected = [
        Token(Tok_Type.OR),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string(".")
    expected = [
        Token(Tok_Type.DOT),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_lexer_errors():
    with pytest.raises(InternalTokenErr):
        lexer = Lexer()
        lexer.tokenize_string("|")

    with pytest.raises(InternalTokenErr):
        lexer = Lexer()
        lexer.tokenize_string("&")

    with pytest.raises(InternalTokenErr):
        lexer = Lexer()
        lexer.tokenize_string("4ab")
