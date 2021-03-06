from zai.lexer import Lexer
from zai.tokens import Tok_Type, Token


def compare_tokens(l1, l2):
    """
    Compare two token lists token by token. Return True if all elements are equal.
    Return False if there is any mismatch.
    """
    # Check length of both lists
    len_l1 = len(l1)
    len_l2 = len(l2)
    assert len_l1 == len_l2

    # Compare element by element
    for idx, token in enumerate(l1):
        assert token == l2[idx]


def test_empty_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("")
    expected = [Token(Tok_Type.EOF)]
    compare_tokens(lexer_output, expected)


def test_special_chars():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("(),;{}[]-+/*'! != = == < <= > >=")
    print(lexer_output)
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


def test_symbol_lex_no_special():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("h")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "h"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("hello")
    print("Lexer output", lexer_output)
    expected = [
        Token(Tok_Type.ID, "hello"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("helloWorld")
    print("Lexer output", lexer_output)
    expected = [
        Token(Tok_Type.ID, "helloWorld"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("MixEDCase")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "MixEDCase"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("symOne symTwo")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "symOne"),
        Token(Tok_Type.ID, "symTwo"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_symbol_lex_special():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("$")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "$"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("@")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "@"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("?")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "?"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("hello@worl$d?")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "hello@worl$d?"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("hello@worl$d?123")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "hello@worl$d?123"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("h3llo@worl$d")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "h3llo@worl$d"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("Symb0lOn3? Symb0lTw0?")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ID, "Symb0lOn3?"),
        Token(Tok_Type.ID, "Symb0lTw0?"),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_number_lex():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string("1")
    print(lexer_output)
    expected = [
        Token(Tok_Type.NUM, 1),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("0")
    print(lexer_output)
    expected = [
        Token(Tok_Type.NUM, 0),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("233")
    print(lexer_output)
    expected = [
        Token(Tok_Type.NUM, 233),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("233 455")
    print(lexer_output)
    expected = [
        Token(Tok_Type.NUM, 233),
        Token(Tok_Type.NUM, 455),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string("-233")
    print(lexer_output)
    expected = [
        Token(Tok_Type.MINUS),
        Token(Tok_Type.NUM, 233),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_string():
    lexer = Lexer()
    lexer_output = lexer.tokenize_string('"hello world"')
    print("RAW LEXER OUTPUT", lexer_output)
    expected = [
        Token(Tok_Type.DQUOTE, None),
        Token(Tok_Type.STRING, "hello world"),
        Token(Tok_Type.DQUOTE, None),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer = Lexer()
    lexer_output = lexer.tokenize_string('"1 number with another number 2"')
    print(lexer_output)
    expected = [
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.STRING, "1 number with another number 2"),
        Token(Tok_Type.DQUOTE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)


def test_keywords():
    lexer = Lexer()

    lexer_output = lexer.tokenize_string("if")
    print(lexer_output)
    expected = [
        Token(Tok_Type.IF),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("while")
    print(lexer_output)
    expected = [
        Token(Tok_Type.WHILE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("for")
    print(lexer_output)
    expected = [
        Token(Tok_Type.FOR),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("print")
    print(lexer_output)
    expected = [
        Token(Tok_Type.PRINT),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("else")
    print(lexer_output)
    expected = [
        Token(Tok_Type.ELSE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("true")
    print(lexer_output)
    expected = [
        Token(Tok_Type.TRUE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("false")
    print(lexer_output)
    expected = [
        Token(Tok_Type.FALSE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("func")
    print(lexer_output)
    expected = [
        Token(Tok_Type.FUNC),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("switch")
    print(lexer_output)
    expected = [
        Token(Tok_Type.SWITCH),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("case")
    print(lexer_output)
    expected = [
        Token(Tok_Type.CASE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("default")
    print(lexer_output)
    expected = [
        Token(Tok_Type.DEFAULT),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("import")
    print(lexer_output)
    expected = [
        Token(Tok_Type.IMPORT),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("as")
    print(lexer_output)
    expected = [
        Token(Tok_Type.AS),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("do")
    print(lexer_output)
    expected = [
        Token(Tok_Type.DO),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("return")
    print(lexer_output)
    expected = [
        Token(Tok_Type.RETURN),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("continue")
    print(lexer_output)
    expected = [
        Token(Tok_Type.CONTINUE),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)

    lexer_output = lexer.tokenize_string("break")
    print(lexer_output)
    expected = [
        Token(Tok_Type.BREAK),
        Token(Tok_Type.EOF),
    ]
    compare_tokens(lexer_output, expected)
