from zai.lexer import Lexer
from zai.tokens import TokType, Token
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
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("\r\n")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)


def test_empty_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)


def test_whitespace_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string(" ")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)

    # 1 TAB
    lexer_output = lexer.tokenize_string("  ")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)

    # 2 TABS
    lexer_output = lexer.tokenize_string("          ")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)


def test_comments():
    lexer = Lexer()

    lexer_output = lexer.tokenize_string("//")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("// // 4 + 4")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("// A comment")
    expected = [Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("abc // A comment")
    expected = [Token(TokType.ID, "abc"), Token(TokType.EOF)]
    compare_tokens(lexer_output, expected)


def test_special_chars():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("(),;{}[]-+/*'! != = == < <= > >=")
    expected = [
        Token(TokType.LROUND),
        Token(TokType.RROUND),
        Token(TokType.COMMA),
        Token(TokType.SEMIC),
        Token(TokType.LCURLY),
        Token(TokType.RCURLY),
        Token(TokType.LSQUARE),
        Token(TokType.RSQUARE),
        Token(TokType.MINUS),
        Token(TokType.PLUS),
        Token(TokType.DIV),
        Token(TokType.MUL),
        Token(TokType.QUOTE),
        Token(TokType.BANG),
        Token(TokType.NEQ),
        Token(TokType.ASSIGN),
        Token(TokType.EQ),
        Token(TokType.LT),
        Token(TokType.LTE),
        Token(TokType.GT),
        Token(TokType.GTE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)


# Symbols without special chars
def test_symbol_lex_no_special():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("h")
    expected = [
        Token(TokType.ID, "h"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("hello")
    expected = [
        Token(TokType.ID, "hello"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("helloWorld")
    expected = [
        Token(TokType.ID, "helloWorld"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("MixEDCase")
    expected = [
        Token(TokType.ID, "MixEDCase"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("symOne symTwo")
    expected = [
        Token(TokType.ID, "symOne"),
        Token(TokType.ID, "symTwo"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_symbol_lex_special():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("$")
    expected = [
        Token(TokType.ID, "$"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("@")
    expected = [
        Token(TokType.ID, "@"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("?")
    expected = [
        Token(TokType.ID, "?"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("hello@worl$d?")
    expected = [
        Token(TokType.ID, "hello@worl$d?"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("hello@worl$d?123")
    expected = [
        Token(TokType.ID, "hello@worl$d?123"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("h3llo@worl$d")
    expected = [
        Token(TokType.ID, "h3llo@worl$d"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("Symb0lOn3? Symb0lTw0?")
    expected = [
        Token(TokType.ID, "Symb0lOn3?"),
        Token(TokType.ID, "Symb0lTw0?"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("one_two")
    expected = [
        Token(TokType.ID, "one_two"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("Symb0lOn3? Symb0lTw0?_three")
    expected = [
        Token(TokType.ID, "Symb0lOn3?"),
        Token(TokType.ID, "Symb0lTw0?_three"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_symbols_mixed_with_numbers():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("mixed_4_sym")
    expected = [
        Token(TokType.ID, "mixed_4_sym"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("@43abc")
    expected = [
        Token(TokType.ID, "@43abc"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("@a4_33$3")
    expected = [
        Token(TokType.ID, "@a4_33$3"),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_number_lex():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("1")
    expected = [
        Token(TokType.NUM, 1),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("0")
    expected = [
        Token(TokType.NUM, 0),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("233")
    expected = [
        Token(TokType.NUM, 233),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("233 455")
    expected = [
        Token(TokType.NUM, 233),
        Token(TokType.NUM, 455),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("-233")
    expected = [
        Token(TokType.MINUS),
        Token(TokType.NUM, 233),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string('"hello world"')
    expected = [
        Token(TokType.DQUOTE, None),
        Token(TokType.STRING, "hello world"),
        Token(TokType.DQUOTE, None),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string('"1 number with another number 2"')
    expected = [
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "1 number with another number 2"),
        Token(TokType.DQUOTE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_language_keywords():
    lexer = Lexer()

    lexer_output = lexer.tokenize_string("if")
    expected = [
        Token(TokType.IF),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("while")
    expected = [
        Token(TokType.WHILE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("for")
    expected = [
        Token(TokType.FOR),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("print")
    expected = [
        Token(TokType.PRINT),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("else")
    expected = [
        Token(TokType.ELSE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("true")
    expected = [
        Token(TokType.TRUE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("false")
    expected = [
        Token(TokType.FALSE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("func")
    expected = [
        Token(TokType.FUNC),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("switch")
    expected = [
        Token(TokType.SWITCH),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("case")
    expected = [
        Token(TokType.CASE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("default")
    expected = [
        Token(TokType.DEFAULT),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("import")
    expected = [
        Token(TokType.IMPORT),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("as")
    expected = [
        Token(TokType.AS),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("do")
    expected = [
        Token(TokType.DO),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("return")
    expected = [
        Token(TokType.RETURN),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("continue")
    expected = [
        Token(TokType.CONTINUE),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("break")
    expected = [
        Token(TokType.BREAK),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("nil")
    expected = [
        Token(TokType.NIL),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("this")
    expected = [
        Token(TokType.THIS),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("or")
    expected = [
        Token(TokType.OR),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("and")
    expected = [
        Token(TokType.AND),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("+=")
    expected = [
        Token(TokType.ADDASSIGN),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("-=")
    expected = [
        Token(TokType.SUBASSIGN),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("++")
    expected = [
        Token(TokType.INCR),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("--")
    expected = [
        Token(TokType.DECR),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("&&")
    expected = [
        Token(TokType.AND),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("||")
    expected = [
        Token(TokType.OR),
        Token(TokType.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string(".")
    expected = [
        Token(TokType.DOT),
        Token(TokType.EOF),
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
