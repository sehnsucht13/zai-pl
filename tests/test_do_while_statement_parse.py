from zai.tokens import TokType, Token
from zai.parse import Parser
import zai.ast_nodes as nodes
from zai.internal_error import InternalParseError
import pytest


def test_properly_formed_do_while():
    tok_stream = [
        Token(TokType.DO),
        Token(TokType.LCURLY),
        Token(TokType.PRINT),
        Token(TokType.INT, 4),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.TRUE),
        Token(TokType.RROUND),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    do_while_node = p.do_while_statement()
    assert isinstance(do_while_node, nodes.DoWhileNode)
    assert isinstance(do_while_node.cond, nodes.BoolNode) and do_while_node.cond.val == TokType.TRUE
    assert isinstance(do_while_node.body, nodes.BlockNode)
    assert isinstance(do_while_node.body.stmnts[0], nodes.PrintNode)


def test_do_while_empty_body():

    tok_stream = [
        Token(TokType.DO),
        Token(TokType.LCURLY),
        Token(TokType.RCURLY),
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.TRUE),
        Token(TokType.RROUND),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    do_while_node = p.do_while_statement()
    assert isinstance(do_while_node, nodes.DoWhileNode)
    assert isinstance(do_while_node.cond, nodes.BoolNode) and do_while_node.cond.val == TokType.TRUE
    assert isinstance(do_while_node.body, nodes.BlockNode)


def test_do_while_missing_body():
    tok_stream = [
        Token(TokType.DO),
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.TRUE),
        Token(TokType.RROUND),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        do_while_node = p.do_while_statement()


def test_do_while_missing_cond():

    tok_stream = [
        Token(TokType.DO),
        Token(TokType.LCURLY),
        Token(TokType.PRINT),
        Token(TokType.INT, 4),
        Token(TokType.SEMIC),
        Token(TokType.RCURLY),
        Token(TokType.WHILE),
        Token(TokType.LROUND),
        Token(TokType.RROUND),
        Token(TokType.SEMIC),
        Token(TokType.EOF),
    ]
    p = Parser(tok_stream, "")
    with pytest.raises(InternalParseError):
        do_while_node = p.do_while_statement()
