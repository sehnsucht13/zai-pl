from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest


def test_well_formed_print():
    tok_stream = [
        Token(TokType.PRINT),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello World"),
        Token(TokType.DQUOTE),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    print_node = p.print_statement()

    assert (
        isinstance(print_node, nodes.PrintNode)
        and isinstance(print_node.expr, nodes.StringNode)
        and print_node.expr.val == "Hello World"
    )


def test_malformed_print():
    # Missing print content
    tok_stream = [
        Token(TokType.PRINT),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        print_node = p.print_statement()

    # Missing Semicolon
    tok_stream = [
        Token(TokType.PRINT),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello World"),
        Token(TokType.DQUOTE),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        print_node = p.print_statement()
