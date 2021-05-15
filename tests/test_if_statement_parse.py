from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest

def test_wellformed_if_statement_with_else():
    tok_stream = [
        Token(TokType.IF),
        Token(TokType.LROUND),
        Token(TokType.TRUE),
        Token(TokType.RROUND),
        Token(TokType.LCURLY),
        Token(TokType.NUM, 4),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.ELSE),
        Token(TokType.LCURLY),
        Token(TokType.DQUOTE),
        Token(TokType.STRING, 4),
        Token(TokType.DQUOTE),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF),
    ]

    p = Parser(tok_stream, "")
    if_node = p.if_statement()
    assert isinstance(if_node, nodes.IfNode)
    assert isinstance(if_node.else_block, nodes.BlockNode)
    for condition in if_node.condition_blocks:
        assert isinstance(condition.test_condition, nodes.BoolNode)
        assert isinstance(condition.body, nodes.BlockNode)


def test_wellformed_if_statement_no_else():
    tok_stream = [
        Token(TokType.IF),
        Token(TokType.LROUND),
        Token(TokType.TRUE),
        Token(TokType.RROUND),
        Token(TokType.LCURLY),
        Token(TokType.NUM, 4),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    if_node = p.if_statement()

    assert isinstance(if_node, nodes.IfNode)
    assert if_node.else_block is None
    for condition in if_node.condition_blocks:
        assert isinstance(condition.test_condition, nodes.BoolNode)
        assert isinstance(condition.body, nodes.BlockNode)


def test_if_statement_missing_condition():
    tok_stream = [
        Token(TokType.IF),
        Token(TokType.LCURLY),
        Token(TokType.NUM, 4),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        if_node = p.if_statement()

def test_if_statement_missing_body():
    tok_stream = [
        Token(TokType.IF),
        Token(TokType.LROUND),
        Token(TokType.TRUE),
        Token(TokType.RROUND),
        Token(TokType.EOF)
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        if_node = p.if_statement()
