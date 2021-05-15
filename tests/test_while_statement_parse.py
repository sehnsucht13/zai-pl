from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest


def test_properly_formed_while():
    tok_stream = [
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.NUM, 1),
        Token(TokType.RROUND),
        Token(TokType.LCURLY),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello world"),
        Token(TokType.DQUOTE),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    while_statement_node = p.while_statement()

    assert isinstance(while_statement_node, nodes.WhileNode) is True
    assert isinstance(while_statement_node.condition, nodes.NumNode) and while_statement_node.condition.val == 1
    assert isinstance(while_statement_node.body, nodes.BlockNode)
    assert (
        isinstance(while_statement_node.body.stmnts[0], nodes.StringNode)
        and while_statement_node.body.stmnts[0].val == "Hello world"
    )


def test_missing_condition_while():
    tok_stream = [
        Token(TokType.WHILE),
        Token(TokType.LCURLY),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello world"),
        Token(TokType.DQUOTE),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        while_statement_node = p.while_statement()


def test_missing_body_while():
    tok_stream = [
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.NUM, 1),
        Token(TokType.RROUND),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        while_statement_node = p.while_statement()


def test_missing_condition_and_body_while():
    tok_stream = [Token(TokType.WHILE), Token(TokType.EOF)]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        while_statement_node = p.while_statement()


def test_improperly_formed_condition_while():
    tok_stream = [
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.NUM, 1),
        Token(TokType.EQ),
        Token(TokType.RROUND),
        Token(TokType.LCURLY),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello world"),
        Token(TokType.DQUOTE),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        while_statement_node = p.while_statement()


def test_improperly_formed_body_while():
    tok_stream = [
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.NUM, 1),
        Token(TokType.RROUND),
        Token(TokType.LCURLY),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, "Hello world"),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        while_statement_node = p.while_statement()
